import os
import time
import config
import asyncio
from dumper import db
from aiogram import Bot
from dumper import Dumper
from datetime import datetime
from encryptor import filecrypt
from dumper.exceptions.no_root_privileges_exception import NoRootPrivilegesException


def start():
    bot = Bot(token=config.bot_token)
    dumper = Dumper(config.backups_path, db.get_connection())

    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_backups(bot, dumper))

        time.sleep(config.backup_interval_hour * 60 * 60)


async def send_backups(bot, dumper):
    try:
        paths = dumper.dump()

        for path in paths:
            if config.enable_rsa_encryption:
                filecrypt.encrypt_file(path, open(config.rsa_public_key_path, 'rb').read(), config.rsa_key_length)

            await bot.send_document(config.your_chat_id, open(path, 'rb'))

            print((
                '[%s] Send backup of %s' %
                (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), os.path.basename(path))) +
                  (' [encrypted]' if config.enable_rsa_encryption else '')
            )

            time.sleep(0.5)

        dumper.clear()
    except NoRootPrivilegesException:
        print('Please run bot as root')
