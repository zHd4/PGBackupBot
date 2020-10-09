import time
import config
from dumper import db
from aiogram import Bot
from dumper import Dumper
from encryptor import filecrypt
from dumper.exceptions.no_root_privileges_exception import NoRootPrivilegesException


def start():
    bot = Bot(token=config.bot_token)
    dumper = Dumper(config.backups_path, db.get_connection())

    while True:
        send_backups(bot, dumper)
        time.sleep(config.backup_interval_hour * 60 * 60)


def send_backups(bot, dumper):
    try:
        paths = dumper.dump()

        for path in paths:
            if config.enable_rsa_encryption:
                filecrypt.encrypt_file(path, config.rsa_public_key.encode('utf-8'), config.rsa_key_length)

            bot.send_document(config.your_chat_id, open(path, 'rb'))
            time.sleep(0.5)

        dumper.clear()
    except NoRootPrivilegesException:
        print('Please run bot as root')
