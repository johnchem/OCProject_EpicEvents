import sys
from sentry_sdk import capture_message, capture_exception
from sqlalchemy.orm import sessionmaker

# views
from epicevents.CLI.cli import cli_handler
from epicevents.CLI.view import Views

# backend
import epicevents.setup as setup
from epicevents.backend.repository import SqlAlchemyRepository
from epicevents.backend.filters import Filters

# controller
from epicevents.controller.controller import Controller
from epicevents.controller.permissions import Permissions

# tools
import epicevents.authentification as auth


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
    setup._create_database()
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


if __name__ == "__main__":
    try:
        globals()[sys.argv[1]]()
    except Exception as err:
        capture_exception(err)
        emmerg_exit()
