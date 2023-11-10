from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from backend.models import User, Client, Contract, Evenement
from backend.models import Departements, ContractStatus

class Filters:
    def by_signed_contract(self, session: Session):
        stmt = select(Contract).where(Contract.contract_status == ContractStatus.SIGNED)
        contracts = session.scalars(stmt).all()
        return contracts

    def by_not_signed_contract(self, session):
        stmt = select(Contract).where(Contract.contract_status == ContractStatus.NOT_SIGNED)
        contracts = session.scalars(stmt).all()
        return contracts

    def by_commercial(self, session, commercial):
        pass