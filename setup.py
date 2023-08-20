import subprocess
import os
from sqlalchemy import create_engine

from settings import SERVER, ADMIN_LOGIN, PORT, DATABASE_NAME, PSQL, PGPASSWORD
from connection import psycopg2_cursor
from models import Base

ADMIN_CREDENTIAL = {
    "database": DATABASE_NAME,
    "user": ADMIN_LOGIN,
    "password": PGPASSWORD,
    "port": PORT,
}


def _create_engine(user, password, port, database):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}", echo=True)
    return engine


def _create_engine_superuser():
    return _create_engine(**ADMIN_CREDENTIAL)


def _create_database():
    # Create table statement
    sql_create_database = "CREATE DATABASE "+DATABASE_NAME+";"

    # Create a table in PostgreSQL database
    cmd = f'"{PSQL}" -h {SERVER} -U {ADMIN_LOGIN} -p {PORT} -c "{sql_create_database}" -w'
    subprocess.run(cmd)


def _create_tables():
    engine = _create_engine_superuser()
    Base.metadata.create_all(engine)


def _drop_tables():
    engine = _create_engine_superuser()
    Base.metadata.drop_all(engine)


def _reinit_tables():
    engine = _create_engine_superuser()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


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
    _reinit_tables()
    # _create_tables(**ADMIN_CREDENTIAL)
    # _drop_tables(**ADMIN_CREDENTIAL)
    print("terminé")
