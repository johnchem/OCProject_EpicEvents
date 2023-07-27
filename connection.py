from functools import wraps
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def psycopg2_cursor(conn_info):
    """Wrap function to setup and tear down a Postgres connection while
    providing a cursor object to make queries with.

    travishathaway/pyscopg2_decorator.py
    """
    def wrap(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Setup postgres connection
                connection = psycopg2.connect(**conn_info)
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()

                # Call function passing in cursor
                return_val = f(cursor, *args, **kwargs)

            finally:
                # Close connection
                connection.close()

            return return_val
        return wrapper
    return wrap
