import sys
from sqlalchemy.orm import sessionmaker

# views
from CLI.view import Views
from CLI.cli import cli_handler

# backend
import setup
from backend.repository import SqlAlchemyRepository
from backend.filters import Filters

# controller
from controller.controller import Controller
from controller.permissions import Permissions


def create_session():
    engine = setup._create_engine_superuser()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def run():
    # views = Views()
    session = create_session()
    filter = Filters()
    repository = SqlAlchemyRepository(session, filter)
    handler = cli_handler()

    views = Views(handler)
    permissions = Permissions()
    app = Controller(repository, views, permissions)
    division_by_zero = 1 / 0
    app.start()


def start_application():
    setup.create_tables()
    print("base de données créés")


def delete_data():
    setup.drop_tables()
    print("Données supprimées")


def reset():
    setup.reinit_tables()
    print("Application réinitialisée")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
