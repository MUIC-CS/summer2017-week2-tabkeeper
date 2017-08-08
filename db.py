from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import os


env = os.getenv('TABKEEPER_ENV', 'development')


def get_password():
    with open('secret') as f:
        return f.read().strip()


setting = {
    'development':  {
        'dbname': 'tabkeeper',
        'user': 'postgres',
        'host': 'localhost',
        'password': ''
    },
    'production':  {
        'dbname': 'tabkeeper',
        'user': 'postgres',
        'host': 'db',
        'password': get_password()
    }
}[env]


pool = ThreadedConnectionPool(1, 20,
                              dbname=setting['dbname'],
                              user=setting['user'],
                              host=setting['host'],
                              password=setting['password'])


@contextmanager
def get_cursor():
    con = pool.getconn()
    try:
        yield con.cursor(cursor_factory=DictCursor)
    finally:
        pool.putconn(con)
