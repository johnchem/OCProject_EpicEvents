from datetime import datetime
import enum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import List

import sqlalchemy.sql.functions as func


class Departements(enum.Enum):
    COMMERCIAL = "Commercial"
    GESTION = "Gestion"
    SUPPORT = "Support"
    ADMIN = "Administrator"

    @classmethod
    def values(cls) -> set:
        return set(i.value for i in cls)


class ContratStatus(enum.Enum):
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
    contrat_portfolio: Mapped[List["Contrat"]] = relationship(back_populates="commercial")
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
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    contrat: Mapped["Contrat"] = relationship(
        back_populates="client",
        lazy="joined",
        cascade="save-update, delete, delete-orphan")
    commercial_contact: Mapped["User"] = relationship(
        back_populates="client_portfolio",
        lazy="joined",
        cascade="save-update")
    evenements: Mapped["Evenement"] = relationship(
        back_populates="client",
        lazy="joined",
        cascade="save-update, delete, delete-orphan")


class Contrat(Base):
    __tablename__ = "contrat"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    commercial_contact_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    total_amount: Mapped[int] = mapped_column(Integer)
    remaining_amount: Mapped[int] = mapped_column(Integer)
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    contrat_status: Mapped[str] = mapped_column(
        Enum(
            ContratStatus,
            values_callable=lambda m: list(m.values())
            )
        )

    client: Mapped["Client"] = relationship(back_populates="contrat", lazy="joined")
    commercial: Mapped["User"] = relationship(back_populates="contrat_portfolio", lazy="joined")
    evenements: Mapped[List["Evenement"]] = relationship(back_populates="contrat", lazy="joined")

    def __init__(self, client, total_amount, remaining_amount, contrat_status):
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.contrat_status = contrat_status
        self.client = client
        self.commercial = client.commercial_contact

    def __repr__(self):
        return f"{self.creation_date} - {self.remaining_amount}/{self.total_amount}"


class Evenement(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrat_id: Mapped[int] = mapped_column(ForeignKey("contrat.id"))
    client_id: Mapped["Client"] = mapped_column(ForeignKey("client.id"))
    event_date_start: Mapped[datetime] = mapped_column(DateTime)
    event_date_end: Mapped[datetime] = mapped_column(DateTime)
    contact_support_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    location: Mapped[str] = mapped_column(String(60))
    attendees: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text)

    client: Mapped["Client"] = relationship(back_populates="evenements", lazy="joined")
    contrat: Mapped["Contrat"] = relationship(back_populates="evenements", lazy="joined")
    contact_support: Mapped["User"] = relationship(back_populates="evenements", lazy="joined")

    @property
    def client_name(self):
        return self.client.company_name

    @property
    def client_contact(self) -> str:
        return self.client.full_name

    def __init__(self, contrat, event_date_start, event_date_end, location, attendees, contact_support, note):
        self.contrat = contrat
        self.client = contrat.client
        self.contact_support = contact_support
        self.event_date_start = event_date_start
        self.event_date_end = event_date_end
        self.location = location
        self.attendees = attendees
        self.note = note
