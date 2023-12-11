from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from backend.models import User, Client, Contract, Evenement
from backend.models import Departements, ContractStatus


class Filters:
    def by_signed_contract(self, session: Session):
        stmt = select(Contract).where(Contract.contract_status == ContractStatus.SIGNED)
        contracts = session.scalars(stmt).unique().all()
        return contracts

    def by_not_signed_contract(self, session):
        stmt = select(Contract).where(Contract.contract_status == ContractStatus.NOT_SIGNED)
        contracts = session.scalars(stmt).unique().all()
        return contracts

    def by_commercial(self, session, commercial):
        stmt = select(Contract).where(Contract.commercial == commercial)
        contracts = session.scalars(stmt).unique().all()
        return contracts

    def commercial_with_contract(self, session):
        stmt = select(User).filter(User.contract_portfolio)
        commercials = session.scalars(stmt).unique().all()
        return commercials

    def contract_not_fully_paid(self, session):
        stmt = select(Contract).filter(Contract.remaining_amount != Contract.total_amount)
        contracts = session.scalars(stmt).unique().all()
        return contracts

    def events_without_support(self, session):
        stmt = select(Evenement).filter(Evenement.contact_support == None)
        events = session.scalars(stmt).unique().all()
        return events

    def event_by_support(self, session, support):
        stmt = select(Evenement).filter(Evenement.contact_support == support)
        events = session.scalars(stmt).unique().all()
        return events
