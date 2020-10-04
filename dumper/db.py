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