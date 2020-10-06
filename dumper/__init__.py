import os
import subprocess
from dumper import env, db
from dumper.exceptions.no_root_privileges_exception import NoRootPrivilegesException


# noinspection PyMethodMayBeStatic
class Dumper:
    def __init__(self, path, db_connection):
        self.__path = path
        self.__db_conn = db_connection

    def dump(self):
        paths = []

        for db_name in db.get_databases(self.__db_conn):
            path = self.__dump_db(self.__path, db_name)

            if db_name is not None:
                paths.append(path)
            else:
                raise NoRootPrivilegesException()

    def __dump_db(self, path, db_name):
        if not env.check_root():
            return None

        db_file_path = os.path.join(path, db_name + '.backup')
        backup_command = 'sudo -u postgres pg_dump %s > %s' % (db_name, db_file_path)

        self.__execute_shell_command(backup_command.split(' '))

        return db_file_path

    def __execute_shell_command(self, command):
        return subprocess.run(command, stdout=subprocess.PIPE)

    def __check_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
