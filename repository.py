import abc
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from models import User, Client, Contrat, Evenement


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, session: Session, data):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, session: Session, user_email):
        raise NotImplementedError

    def get_client(self, session: Session, client_name):
        raise NotImplementedError

    def get_contract(self, session: Session, contract_status, client_name):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, session, data):
        session.add(data)

    def add_bulk(self, session: Session, list_data: list):
        for data in list_data:
            session.add(data)

    def get_user(self, session: Session, user_email: str):
        return session.query(User).filter_by(email=user_email).first()

    def list_user(self, session: Session):
        return session.query(User).all()

    def update_user(self, session: Session, user_id: int):
        yield session.query(User).filter_by(user_id=user_id).first()
        session.execute(select(User).where(user_id == user_id))

    def get_client(self, session: Session, client_name):
        stmt = select(Client).options(joinedload(Client.commercial_contact)).filter_by(full_name=client_name)
        return session.scalars(stmt).unique().first()

    def list_client(self, session: Session):
        return session.query(Client).all()

    def update_client(self, session: Session, client_id):
        yield session.query(Client).filter_by(client_id=client_id).first()
        session.execute(select(Client).where(client_id == client_id))

    def get_contract(self, session: Session, contract_status, client_name):
        client = session.query(Client).filter_by(full_name=client_name).first()
        stmt = select(Contrat).options(joinedload(Contrat.client)).filter_by(contrat_status=contract_status).filter_by(client=client)
        return session.scalars(stmt).unique().first()

