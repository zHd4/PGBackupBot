import subprocess


def execute_shell_command(command):
    return subprocess.run(command, stdout=subprocess.PIPE)


def dump_db(db_name):
    backup_command = 'sudo -u postgres pg_dump %s > %s' % (db_name, db_name + '.backup')
    execute_shell_command(backup_command.split(' '))
