import atexit
import sys
from sentry_sdk import capture_message
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

# tools 
import authentification as auth


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
    app.start()


def start_application():
    setup.create_tables()
    print("base de données créés")


def delete_data():
    # clean DB w/ deleting the tables
    setup.drop_tables()
    print("Données supprimées")


def reset():
    # delete all tables and data; fresh start
    setup.reinit_tables()
    print("Application réinitialisée")

def emmerg_exit():
    # In case of crash : record event and remove login token
    auth.remove_token_file()
    msg = "Emergency Stop - Clean up token"
    capture_message(msg)
    print(msg)


if __name__ == "__main__":
    try :
        globals()[sys.argv[1]]()
    except Exception as err:
        emmerg_exit()