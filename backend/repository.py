from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from backend.models import User, Client, Contract, Evenement
import authentification as auth


class SqlAlchemyRepository():
    def __init__(self, session: Session):
        self.session = session

    def add(self, data):
        self.session.add(data)
        return True

    def add_bulk(self, list_data: list):
        for data in list_data:
            self.session.add(data)
        return True

    def commit(self):
        self.session.commit()
        return True

    def get_user(self, user_email: str):
        return self.session.query(User).filter_by(email=user_email).first()

    def user_login(self, user_email, password):
        try:
            user = self.get_user(user_email)
            if auth.authenticate_user(user, password):
                return user
            return False
        except Exception as err:
            print(err)
            print("ce compte n'existe pas")

    def list_user(self):
        stmt = select(User).order_by(User.id)
        return self.session.scalars(stmt).unique().all()
        # return self.session.query(User).all()

    def delete_user(self, user_data):
        stmt = select(User).where(User.id == user_data.id)
        user = self.session.scalars(stmt).one()
        self.session.delete(user)
        self.session.commit()
        return True

    def get_client(self, client_name: str):
        stmt = select(Client).options(joinedload(Client.commercial_contact)).filter_by(full_name=client_name)
        return self.session.scalars(stmt).unique().first()

    def list_client(self):
        stmt = select(Client).order_by(Client.id)
        return self.session.scalars(stmt).unique().all()
        # return self.session.query(Client).all()

    def delete_client(self, client_id: int):
        stmt = select(Client).where(Client.id == client_id)
        client = self.session.scalars(stmt).first()
        self.session.delete(client)
        self.session.commit()
        return True

    def get_contract(self, contract_id):
        stmt = select(Contract).filter_by(contract_id)
        return self.session.scalars(stmt).first()

    def list_contract(self):
        stmt = select(Contract).order_by(Contract.id)
        return self.session.scalars(stmt).unique().all()
        # return self.session.query(contract).all()

    def delete_contract(self, contract_id: int):
        stmt = select(Contract).where(Contract.id == contract_id)
        client = self.session.scalars(stmt).first()
        self.session.delete(client)
        return True

    def get_event(self, event_id: int):
        stmt = select(Evenement).filter_by(id=event_id)
        return self.session.scalars(stmt).unique().first()

    def list_event(self):
        stmt = select(Evenement).order_by(Evenement.id)
        return self.session.scalars(stmt).all()

    def delete_event(self, event_id: int):
        stmt = select(Evenement).where(Evenement.id == event_id)
        event = self.session.scalars(stmt).first()
        self.session.delete(event)
        return True

    # def get_event_by_client(self, session: Session, client_name):
    #     client = session.query(Client).filter(full_name=client_name)
    #     stmt = select(Evenement).options(joinedload(Evenement.client)).filter_by(client=client).first()
    #     return session.scalars(stmt).unique().first()

    # def get_event_by_support(self, session: Session, support_email):
    #     user = session.query(User).filter_by(email=support_email)
    #     stmt = select(Evenement).option(joinedload(Evenement.contact_support)).filter_by(contact_support=user).first()
    #     return session.scalars(stmt).unique().first()
