import config
import psycopg2


class Database:
    def __init__(self, host, port, login, password, database):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                user=login,
                password=password,
                database=database
            )
        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to PostgreSQL', error)


def get_connection():
    return Database(config.pg_host, config.pg_port, config.pg_login, config.pg_password, 'postgres')


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def get_databases(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT datname FROM pg_database")  # postgres template0 template1

    databases = []

    for db in cursor.fetchall():
        db = str(db[0])

        if db is not 'postgres' or 'template0' or 'template1':
            databases.append(db)
