from datetime import datetime
import enum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import validates
from typing import List

import sqlalchemy.sql.functions as func

DT_STRING = "%d/%m/%Y %H:%M:%S"


class Departements(enum.Enum):
    COMMERCIAL = "Commercial"
    GESTION = "Gestion"
    SUPPORT = "Support"
    ADMIN = "Administrator"

    @classmethod
    def values(cls) -> set:
        return set(i.value for i in cls)


class ContractStatus(enum.Enum):
    SIGNED = "Contrat signé"
    NOT_SIGNED = "Contrat en cours"

    @classmethod
    def values(cls) -> set:
        return set(i.value for i in cls)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    forname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column()
    departement: Mapped[str] = mapped_column(
        Enum(
            Departements,
            # values_callable=lambda m: list(m.values())
            )
        )

    client_portfolio: Mapped[List["Client"]] = relationship(back_populates="commercial_contact")
    contract_portfolio: Mapped[List["Contract"]] = relationship(back_populates="commercial")
    evenements: Mapped[List["Evenement"]] = relationship(back_populates="contact_support")

    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.name}, forname={self.forname}, dpt={self.departement})'


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(10))
    company_name: Mapped[str] = mapped_column(String(60))
    _creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )
    _last_update: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now()
        )
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    contract: Mapped[List["Contract"]] = relationship(
        back_populates="client",
        lazy="joined",
        cascade="save-update, delete, delete-orphan")
    commercial_contact: Mapped["User"] = relationship(
        back_populates="client_portfolio",
        foreign_keys=[commercial_contact_id],
        lazy="joined",
        cascade="save-update")
    evenements: Mapped[list["Evenement"]] = relationship(
        back_populates="client",
        lazy="joined",
        cascade="save-update, delete, delete-orphan")

    @property
    def creation_date(self):
        return self._creation_date.strftime(DT_STRING)

    @creation_date.setter
    def creation_date(self, date_time):
        date_time = date_time.strftime(DT_STRING)
        self._creation_date = date_time

    @property
    def last_update(self):
        return self._last_update.strftime(DT_STRING)

    @last_update.setter
    def last_update(self, date_time):
        last_update = date_time.strftime(DT_STRING)
        self._last_update = last_update

    # @validates("commercial_contact")
    # def validate_commercial_contact(self, key, commercial):
    #     if commercial.departement is not Departements.COMMERCIAL:
    #         raise ValueError("Ce membre ne fait pas partis de l'équipe commercial")
    #     return commercial


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    commercial_contact_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    total_amount: Mapped[int] = mapped_column(Integer)
    remaining_amount: Mapped[int] = mapped_column(Integer)
    _creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
        )
    contract_status: Mapped[str] = mapped_column(
        Enum(
            ContractStatus,
            values_callable=lambda m: list(m.values())
            )
        )

    client: Mapped["Client"] = relationship(back_populates="contract", lazy="joined")
    commercial: Mapped["User"] = relationship(back_populates="contract_portfolio", lazy="joined")
    evenement: Mapped["Evenement"] = relationship(back_populates="contract", lazy="joined")

    def __init__(self, client, total_amount, remaining_amount, contract_status):
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.contract_status = contract_status
        self.client = client
        self.commercial = client.commercial_contact

    def __repr__(self):
        return f"{self.creation_date} - {self.remaining_amount}/{self.total_amount}"

    @property
    def creation_date(self):
        return self._creation_date.strftime(DT_STRING)

    @creation_date.setter
    def creation_date(self, date_time):
        date_time = date_time.strftime(DT_STRING)
        self._creation_date = date_time


class Evenement(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id"))
    client_id: Mapped["Client"] = mapped_column(ForeignKey("client.id"))
    _event_date_start: Mapped[datetime] = mapped_column(DateTime)
    _event_date_end: Mapped[datetime] = mapped_column(DateTime)
    contact_support_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    location: Mapped[str] = mapped_column(String(60))
    attendees: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text)

    client: Mapped["Client"] = relationship(back_populates="evenements", lazy="joined")
    contract: Mapped["Contract"] = relationship(back_populates="evenement", lazy="joined")
    contact_support: Mapped["User"] = relationship(back_populates="evenements", lazy="joined")

    @property
    def event_date_start(self):
        return self._event_date_start.strftime(DT_STRING)

    @event_date_start.setter
    def event_date_start(self, date_time):
        date_time = date_time.strftime(DT_STRING)
        self._event_date_start = date_time

    @property
    def event_date_end(self):
        return self._event_date_end.strftime(DT_STRING)

    @event_date_end.setter
    def event_date_end(self, date_time):
        date_time = date_time.strftime(DT_STRING)
        self._event_date_end = date_time

    # @property
    # def client_name(self):
    #     return self.client.company_name

    # @property
    # def client_contact(self) -> str:
    #     return self.client.full_name

    # def __init__(self, contract, event_date_start, event_date_end, location, attendees, contact_support, note):
    #     self.contract = contract
    #     self.client = contract.client
    #     self.contact_support = contact_support
    #     self.event_date_start = event_date_start
    #     self.event_date_end = event_date_end
    #     self.location = location
    #     self.attendees = attendees
    #     self.note = note
