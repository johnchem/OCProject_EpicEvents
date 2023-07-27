from datetime import datetime
import enum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy import types, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sqlalchemy.sql.functions as func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    class Departements(enum.Enum):
        COMMERCIAL = "Commercial"
        GESTION = "Gestion"
        SUPPORT = "Support"

        @classmethod
        def values(cls) -> set:
            return set(i.value for i in cls)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    forname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    departement: Mapped[str] = mapped_column(
        Enum(
            Departements,
            values_callable=lambda m: list(m.values())
            )
        )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, ",
            f"name={self.name!r}, ",
            f"forname={self.forname!r}, ",
            f"dpt={self.departement!r})"
        )


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

    commercial_contact: Mapped["User"] = relationship()

    def __init__(self, name, email, phone, company_name, commercial_email):
        self.full_name = name
        self.email = email
        self.phone = phone
        self.company_name = company_name
        self.commercial_contact = User(email=commercial_email)


class Contrat(Base):
    __tablename__ = "contrat"

    class ContratStatus(enum.Enum):
        SIGNED = "Contrat signé"
        NOT_SIGNED = "Contrat en cours"

        @classmethod
        def values(cls) -> set:
            return set(i.value for i in cls)

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

    client: Mapped["Client"] = relationship()
    commercial: Mapped["User"] = relationship()

    @property
    def commercial_contact(self):
        return self.client.commercial_contact


class Evenement(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrat_id: Mapped[int] = mapped_column(ForeignKey("contrat.id"))
    # client_contact: Mapped["Client"] = mapped_column(ForeignKey("client.id"))
    # client_name: Mapped[str] = column_property(
    #     select(Client.full_name)
    #     .where(Client.company_name == client_contact)
    # )
    event_date_start: Mapped[datetime] = mapped_column(DateTime)
    event_date_end: Mapped[datetime] = mapped_column(DateTime)
    contact_support_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    location: Mapped[str] = mapped_column(String(60))
    attendees: Mapped[int] = mapped_column(Integer)
    note: Mapped[str] = mapped_column(Text)

    client: Mapped["User"] = relationship()
    contrat: Mapped["Contrat"] = relationship()
    contact_support: Mapped["User"] = relationship()

    @property
    def client_name(self):
        return self.client.company_name

    @property
    def client_contact(self) -> str:
        return self.client.full_name
