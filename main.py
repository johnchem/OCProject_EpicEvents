import sys
from sqlalchemy.orm import sessionmaker

# views
from CLI.view import Views
from CLI.cli import cli_handler

# backend
from backend.repository import SqlAlchemyRepository
import setup

# controller
from controller.controller import Controller


def create_session():
    engine = setup._create_engine_superuser()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def run():
    # views = Views()
    session = create_session()
    repository = SqlAlchemyRepository(session)
    handler = cli_handler()

    views = Views(handler)
    app = Controller(repository, views)
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
