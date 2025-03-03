import os
from dumper import env, db
from datetime import datetime
from dumper.exceptions.no_root_privileges_exception import NoRootPrivilegesException


# noinspection PyMethodMayBeStatic
class Dumper:
    def __init__(self, path, db_connection):
        self.__path = path
        self.__paths_of_dumped_dbs = []
        self.__db_conn = db_connection

        self.__check_path(path)

    def dump(self):
        paths = []

        for db_name in db.get_databases(self.__db_conn):
            path = self.__dump_db(self.__path, db_name)

            if path is not None:
                paths.append(path)
            else:
                raise NoRootPrivilegesException()

        self.__paths_of_dumped_dbs = paths

        return paths

    def clear(self):
        for path in self.__paths_of_dumped_dbs:
            os.remove(path)

    def __dump_db(self, path, db_name):
        if not env.check_root():
            return None

        db_file_path = os.path.join(path, db_name + '_' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + '.backup')
        backup_command = 'sudo -u postgres pg_dump %s > %s' % (db_name, db_file_path)

        self.__execute_shell_command(backup_command)

        return db_file_path

    def __execute_shell_command(self, command):
        return os.system(command)

    def __check_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)
