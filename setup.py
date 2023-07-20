import psycopg2
import subprocess
import os

from settings import SERVER, ADMIN_LOGIN, PORT, DATABASE_NAME, PSQL, PGPASSWORD
from connection import psycopg2_cursor

ADMIN_CREDENTIAL = {
    "database": DATABASE_NAME,
    "user": ADMIN_LOGIN,
    "password": PGPASSWORD,
    "port": PORT,
}


def _create_database():
    # Create table statement
    sql_create_database = "CREATE DATABASE "+DATABASE_NAME+";"

    # Create a table in PostgreSQL database
    cmd = f'"{PSQL}" -h {SERVER} -U {ADMIN_LOGIN} -p {PORT} -c "{sql_create_database}" -w'
    subprocess.run(cmd)


@psycopg2_cursor(ADMIN_CREDENTIAL)
def test_print(cursor):
    # execute a statement
    print('PostgreSQL database version:')
    cursor.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cursor.fetchone()
    print(db_version)


@psycopg2_cursor(ADMIN_CREDENTIAL)
def _create_user(cursor, login, password, team):

    os.system(f'CREATE USER {DATABASE_NAME} WITH PASSWORD {password};')
    os.system(f"ALTER ROLE {login} SET client_encoding TO 'utf8';")
    os.system(f"ALTER ROLE {login} SET defaut_transaction_isolation TO 'read committed';")
    os.system(f"ALTER ROLE {login} SET timezone TO 'Europe/Paris';")
    os.system(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_NAME} TO {login};")


if __name__ == "__main__":
    test_print()
    print("terminé")
