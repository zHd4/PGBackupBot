import os
import subprocess
from dumper import env, db


# noinspection PyMethodMayBeStatic
class Dumper:
    def dump(self):
        for db_name in db.get_databases(db.get_connection()):
            pass

    def dump_db(self, path, db_name):
        if not env.check_root():
            return None

        db_file_path = os.path.join(path, db_name + '.backup')
        backup_command = 'sudo -u postgres pg_dump %s > %s' % (db_name, db_file_path)

        self.execute_shell_command(backup_command.split(' '))

        return db_file_path

    def execute_shell_command(self, command):
        return subprocess.run(command, stdout=subprocess.PIPE)

    def check_path(self, path):
        return os.path.exists(self, path)
