import subprocess
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sentry_sdk

from epicevents.backend.models import User, Departements

from epicevents.settings import (
    SERVER,
    ADMIN_LOGIN,
    PORT,
    DATABASE_NAME,
    PSQL,
    PGPASSWORD,
    SENTRY_KEY,
)
from epicevents.backend.models import Base

ADMIN_CREDENTIAL = {
    "database": DATABASE_NAME,
    "user": ADMIN_LOGIN,
    "password": PGPASSWORD,
    "port": PORT,
}

sentry_sdk.init(
    dsn=SENTRY_KEY,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    enable_tracing=True,
)


def _create_engine(user, password, port, database):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}", echo=False)
    return engine


def _create_engine_superuser():
    return _create_engine(**ADMIN_CREDENTIAL)


# def _create_test_engine():
# return _create_engine(**TEST_CREDENTIAL)


def _create_general_user():
    _user = User(
        name="admin",
        forname="admin",
        email="admin@epicevents.com",
        password="admin",
        departement=Departements.ADMIN,
    )
    return _user


def _create_database():
    # Create table statement
    sql_create_database = "CREATE DATABASE " + DATABASE_NAME + ";"

    # Create a table in PostgreSQL database
    cmd = f'"{PSQL}" -h {SERVER} -U {ADMIN_LOGIN} -p {PORT} -c "{sql_create_database}" -w'
    subprocess.run(cmd)


def create_tables():
    engine = _create_engine_superuser()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = _create_general_user()
    session.add(user)
    session.commit()


def drop_tables():
    engine = _create_engine_superuser()
    Base.metadata.drop_all(engine)


def reinit_tables():
    engine = _create_engine_superuser()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    user = _create_general_user()
    session.add(user)
    session.commit()


def _create_user_db(cursor, login, password, team):
    os.system(f"CREATE USER {DATABASE_NAME} WITH PASSWORD {password};")
    os.system(f"ALTER ROLE {login} SET client_encoding TO 'utf8';")
    os.system(f"ALTER ROLE {login} SET defaut_transaction_isolation TO 'read committed';")
    os.system(f"ALTER ROLE {login} SET timezone TO 'Europe/Paris';")
    os.system(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_NAME} TO {login};")


if __name__ == "__main__":
    pass
