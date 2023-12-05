from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
import sqlalchemy.exc
import psycopg2
import sentry_sdk
from sentry_sdk import capture_exception

from backend.models import User, Client, Contract, Evenement
import authentification as auth


class SqlAlchemyRepository:
    def __init__(self, session: Session, filter):
        self.session = session
        self.filter = filter

    def add(self, data):
        with sentry_sdk.start_transaction(name="add"):
            try:
                self.session.add(data)
                self.session.commit()
            except sqlalchemy.exc.IntegrityError as err:
                if err.orig is psycopg2.errors.UniqueViolation:
                    msg = "Cette utilisateur existe déjà !"
                return False, msg
            except Exception as err:
                msg = f"erreur survenue lors de la création : {err}"
                capture_exception(err)
                return False, msg
            else:
                return True, None

    def add_bulk(self, list_data: list):
        try:
            for data in list_data:
                self.session.add(data)

        except sqlalchemy.exc.IntegrityError as err:
            if err.orig is psycopg2.errors.UniqueViolation:
                msg = "Cette utilisateur existe déjà !"
            return False, msg
        except Exception as err:
            msg = f"erreur survenue lors de la création : {err}"
            capture_exception(err)
            return False, msg

    def commit(self):
        try:
            self.session.commit()
            return True, None
        except Exception as err:
            capture_exception(err)
            return False, err

    def get_user(self, user_email: str):
        with sentry_sdk.start_transaction(name="get_user"):
            user = self.session.query(User).filter_by(email=user_email).first()
            return user

    def list_user(self):
        with sentry_sdk.start_transaction(name="list_user"):
            stmt = select(User).order_by(User.id)
            return self.session.scalars(stmt).unique().all()

    def delete_user(self, user_data):
        with sentry_sdk.start_transaction(name="delete_user"):
            try:
                stmt = select(User).where(User.id == user_data.id)
                user = self.session.scalars(stmt).unique().one()
                self.session.delete(user)
                self.session.commit()
                return True, None
            except Exception as err:
                capture_exception(err)
                msg = "erreur lors de la suppression"
                return False, msg

    def get_client(self, client_name: str):
        with sentry_sdk.start_transaction(name="get_client"):
            stmt = select(Client).options(joinedload(Client.commercial_contact)).filter_by(full_name=client_name)
            return self.session.scalars(stmt).unique().first()

    def list_client(self):
        with sentry_sdk.start_transaction(name="list_client"):
            stmt = select(Client).order_by(Client.id)
            return self.session.scalars(stmt).unique().all()

    def delete_client(self, client_id: int):
        with sentry_sdk.start_transaction(name="delete_client"):
            try:
                stmt = select(Client).where(Client.id == client_id)
                client = self.session.scalars(stmt).first()
                self.session.delete(client)
                self.session.commit()
                return True, None
            except Exception as err:
                capture_exception(err)
                msg = "erreur lors de la suppression du client"
                return False, msg

    def get_contract(self, contract_id):
        with sentry_sdk.start_transaction(name="get_contract"):
            stmt = select(Contract).filter_by(contract_id)
            return self.session.scalars(stmt).first()

    def list_contract(self):
        with sentry_sdk.start_transaction(name="list_contract"):
            stmt = select(Contract).order_by(Contract.id)
            return self.session.scalars(stmt).unique().all()

    def delete_contract(self, contract_id: int):
        with sentry_sdk.start_transaction(name="delete_contract"):
            try:
                stmt = select(Contract).where(Contract.id == contract_id)
                client = self.session.scalars(stmt).first()
                self.session.delete(client)
                self.session.commit()
                return True, None
            except Exception as err:
                capture_exception(err)
                msg = "Erreur durant la suppression du contrat"
                return False, msg

    def get_event(self, event_id: int):
        with sentry_sdk.start_transaction(name="get_event"):
            stmt = select(Evenement).filter_by(id=event_id)
            return self.session.scalars(stmt).unique().first()

    def list_event(self):
        with sentry_sdk.start_transaction(name="list_event"):
            stmt = select(Evenement).order_by(Evenement.id)
            return self.session.scalars(stmt).all()

    def delete_event(self, event_id: int):
        with sentry_sdk.start_transaction(name="delete_event"):
            try:
                stmt = select(Evenement).where(Evenement.id == event_id)
                event = self.session.scalars(stmt).first()
                self.session.delete(event)
                self.session.commit()
                return True, None
            except Exception as err:
                capture_exception(err)
                msg = "Erreur durant la suppression de l'évenement"
                return False, msg

    def filter_by_signed_contract(self):
        with sentry_sdk.start_transaction(name="filter_by_signed_contract"):
            contracts = self.filter.by_signed_contract(self.session)
            return contracts

    def filter_by_not_signed_contract(self):
        with sentry_sdk.start_transaction(name="filter_by_not_signed_contract"):
            contracts = self.filter.by_not_signed_contract(self.session)
            return contracts

    def filter_contract_by_commercial(self, commercial):
        with sentry_sdk.start_transaction(name="filter_contract_by_commercial"):
            contracts = self.filter.by_commercial(self.session, commercial)
            return contracts

    def list_commercial_with_contract(self):
        with sentry_sdk.start_transaction(name="list_commercial_with_contract"):
            commercials = self.filter.commercial_with_contract(self.session)
            return commercials

    def filter_events_without_support(self):
        with sentry_sdk.start_transaction(name="filter_events_without_support"):
            events = self.filter.events_without_support(self.session)
            return events

    def filter_events_by_support(self, support):
        with sentry_sdk.start_transaction(name="filter_events_by_support"):
            events = self.filter.event_by_support(self.session, support)
            return events
