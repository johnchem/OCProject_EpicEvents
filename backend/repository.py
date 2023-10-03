from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from backend.models import User, Client, Contrat, Evenement
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
        except:
            print("ce compte n'existe pas")

    def list_user(self):
        return self.session.query(User).all()

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
        return self.session.query(Client).all()

    def update_client(self, client_id: int):
        stmt = select(Client).where(Client.id == client_id)
        yield self.session.scalars(stmt).unique().first()
        self.session.commit()
        return True

    def delete_client(self, client_id: int):
        stmt = select(Client).where(Client.id == client_id)
        client = self.session.scalars(stmt).first()
        self.session.delete(client)
        self.session.commit()
        return True

    def get_contract(self, contract_status, client_name):
        client = self.session.query(Client).filter_by(full_name=client_name).first()
        stmt = select(Contrat).\
            options(joinedload(Contrat.client)).\
            filter_by(contrat_status=contract_status).\
            filter_by(client=client)
        return self.session.scalars(stmt).unique().first()

    def list_contract(self):
        contrat = self.session.query(Contrat).all()
        return contrat

    def update_contrat(self, contrat_id: int):
        stmt = select(Contrat).where(Contrat.id == contrat_id)
        yield self.session.scalars(stmt).first()
        self.session.commit()
        return True

    def delete_contrat(self, contrat_id: int):
        stmt = select(Contrat).where(Contrat.id == contrat_id)
        client = self.session.scalars(stmt).first()
        self.session.delete(client)
        return True

    def get_event_by_client(self, session: Session, client_name):
        client = session.query(Client).filter(full_name=client_name)
        stmt = select(Evenement).options(joinedload(Evenement.client)).filter_by(client=client).first()
        return session.scalars(stmt).unique().first()

    def get_event_by_support(self, session: Session, support_email):
        user = session.query(User).filter_by(email=support_email)
        stmt = select(Evenement).option(joinedload(Evenement.contact_support)).filter_by(contact_support=user).first()
        return session.scalars(stmt).unique().first()
