from sqlalchemy import select
from sqlalchemy.orm import Session, lazyload, joinedload
from models import User, Client, Contrat, Evenement
from datetime import datetime

from setup import _create_engine_superuser

DT_STRING = "%d/%m/%Y %H:%M:%S"


def _add_all(list_data):
    engine = _create_engine_superuser()

    with Session(engine) as session:
        for data in list_data:
            session.add(data)
            session.commit()


def _get_user(user_email):
    engine = _create_engine_superuser()

    with Session(engine) as session:
        return session.query(User).filter_by(email=user_email).first()


def _get_client(client_name):
    engine = _create_engine_superuser()

    with Session(engine) as session:
        stmt = select(Client).options(joinedload(Client.commercial_contact)).filter_by(full_name=client_name)
        client = session.scalars(stmt).unique().first()
        return client


def _get_contract(contract_status, client_name):
    engine = _create_engine_superuser()
    # client=session.query(Client).filter_by(full_name="roule maboule").first()

    with Session(engine) as session:
        client = session.query(Client).filter_by(full_name=client_name).first()
        stmt = select(Contrat).options(joinedload(Contrat.client)).filter_by(contrat_status=contract_status).filter_by(client=client)
        contract = session.scalars(stmt).unique().first()
        return contract


def user_items():
    paul = User(
        name="paul",
        forname="test",
        email="paul@test1.com",
        departement="Commercial",
    )

    jean = User(
        name="jean",
        forname="test",
        email="jean@test1.com",
        departement="Commercial"
    )

    george = User(
        name="george",
        forname="test",
        email="george@test2.com",
        departement="Gestion"
    )

    michel = User(
        name="michel",
        forname="test",
        email="michel@test3.com",
        departement="Support"
    )
    return [paul, jean, george, michel]


def client_items():
    bowling_cie_1 = Client(
        full_name="roule maboule",
        email="rmaboule@bowling.com",
        phone="0123456789",
        company_name="Bowling & Cie",
        commercial_contact=_get_user("paul@test1.com"),
    )

    bowling_cie_2 = Client(
        full_name="rouli bouli",
        email="rbouli@bowling.com",
        phone="0123456789",
        company_name="Bowling & Cie",
        commercial_contact=_get_user("jean@test1.com"),
    )

    staple_hero = Client(
        full_name="jean nemarre",
        email="jnemarre@staplehero.com",
        phone="0123456789",
        company_name="StapleHero",
        commercial_contact=_get_user("paul@test1.com"),
    )
    return [bowling_cie_1, bowling_cie_2, staple_hero]


def contrat_items():
    contrat_bowling = Contrat(
        client=_get_client("roule maboule"),
        total_amount=10000,
        remaining_amount=250,
        contrat_status="Contrat signé"
    )

    contrat_staple = Contrat(
        client=_get_client("jean nemarre"),
        total_amount=25000,
        remaining_amount=25000,
        contrat_status="Contrat en cours",
    )
    return [contrat_bowling, contrat_staple]


def evenement_items():
    drink = Evenement(
        contrat=_get_contract("Contrat signé", "roule maboule"),
        event_date_start=datetime.strptime("01/05/2025 10:25:00", DT_STRING),
        event_date_end=datetime.strptime("06/05/2025 10:25:00", DT_STRING),
        location="bali-bali",
        attendees=10,
        contact_support=_get_user("michel@test3.com"), 
        note="les chefs se la coule douce",
    )
    return [drink]


if __name__ == "__main__":

    # user = user_items()

    # client = client_items()

    # contrat_data = contrat_items()

    # event_data = [
    #     drink,
    # ]

    # _add_all(user_items())
    # _add_all(client_items())
    # _add_all(contrat_items())
    _add_all(evenement_items())

    print("job done !")
