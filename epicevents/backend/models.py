from datetime import datetime
import enum
import sqlalchemy.sql.functions as func
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List


DT_STRING = "%d/%m/%Y %H:%M"


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
        )
    )

    client_portfolio: Mapped[List["Client"]] = relationship(
        back_populates="commercial_contact",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    contract_portfolio: Mapped[List["Contract"]] = relationship(
        back_populates="commercial",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    evenements: Mapped[List["Evenement"]] = relationship(
        back_populates="contact_support",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, forname={self.forname}, dpt={self.departement})"


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(10))
    company_name: Mapped[str] = mapped_column(String(60))
    _creation_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    _last_update: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    contract: Mapped[List["Contract"]] = relationship(
        back_populates="client", lazy="joined", cascade="all, delete-orphan"
    )
    commercial_contact: Mapped["User"] = relationship(
        back_populates="client_portfolio", foreign_keys=[commercial_contact_id], lazy="joined", cascade="save-update"
    )
    evenements: Mapped[List["Evenement"]] = relationship(
        back_populates="client", lazy="joined", cascade="all, delete-orphan"
    )

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


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    commercial_contact_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    total_amount: Mapped[int] = mapped_column(Integer)
    remaining_amount: Mapped[int] = mapped_column(Integer)
    _creation_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    contract_status: Mapped[str] = mapped_column(
        Enum(
            ContractStatus,
            # values_callable=lambda m: list(m.values())
        )
    )

    client: Mapped["Client"] = relationship(
        back_populates="contract",
        foreign_keys=[client_id],
        lazy="joined",
        cascade="save-update",
    )
    commercial: Mapped["User"] = relationship(
        back_populates="contract_portfolio",
        foreign_keys=[commercial_contact_id],
        lazy="joined",
        cascade="save-update",
    )
    evenement: Mapped["Evenement"] = relationship(
        back_populates="contract", lazy="joined", cascade="all, delete-orphan"
    )

    def __init__(self, client, total_amount, remaining_amount, contract_status):
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.contract_status = contract_status
        self.client = client
        self.commercial = client.commercial_contact

    def __repr__(self):
        return f"{self.client.full_name} - {self.contract_status.value}"

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
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    _event_date_start: Mapped[datetime] = mapped_column(DateTime)
    _event_date_end: Mapped[datetime] = mapped_column(DateTime)
    contact_support_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    location: Mapped[str] = mapped_column(String(60))
    attendees: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text, nullable=True)

    client: Mapped["Client"] = relationship(
        back_populates="evenements",
        foreign_keys=[client_id],
        lazy="joined",
        cascade="save-update",
    )
    contract: Mapped["Contract"] = relationship(
        back_populates="evenement",
        foreign_keys=[contract_id],
        lazy="joined",
        cascade="save-update",
    )
    contact_support: Mapped["User"] = relationship(
        back_populates="evenements",
        lazy="joined",
        cascade="save-update",
    )

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
