import time
import config
from dumper import db
from aiogram import Bot
from dumper import Dumper
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
    except NoRootPrivilegesException:
        print('Please run bot as root')
