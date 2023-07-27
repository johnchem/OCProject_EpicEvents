from sqlalchemy.orm import Session
from create_table import User, Client, Contrat, Evenement
from datetime import datetime

from setup import _create_engine_superuser

DT_STRING = "%d/%m/%Y %H:%M:%S"

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

bowling_cie = Client(
    name="roule maboule",
    email="rmaboule@bowling.com",
    phone="0123456789",
    company_name="Bowling & Cie",
    commercial_email="paul@test1.com",
)

bowling_cie = Client(
    name="rouli bouli",
    email="rbouli@bowling.com",
    phone="0123456789",
    company_name="Bowling & Cie",
    commercial_email="jean@test1.com",
)

staple_hero = Client(
    name="jean nemarre",
    email="jnemarre@staplehero.com",
    phone="0123456789",
    company_name="StapleHero",
    commercial_email="paul@test1.com",
)

# contrat_bowling = Contrat(
#     client=Client(full_name="roule maboule"),
#     total_amount=10000,
#     remaining_amount=250,
#     contrat_status="Contrat signé"
# )

# contrat_staple = Contrat(
#     client=Client(full_name="jean nemarre"),
#     total_amount=25000,
#     remaining_amount=25000,
#     contrat_status="Contrat en cours",
# )

# drink = Evenement(
#     contrat_id=Contrat(contrat_status="Contrat signé"),
#     event_date_start=datetime.strptime("01/05/2025 10:25:00", DT_STRING),
#     event_date_end=datetime.strptime("06/05/2025 10:25:00", DT_STRING),
#     location="bali-bali",
#     attendees=10,
#     note="les chefs se la coule douce",
# )


def _add_all(list_data):
    engine = _create_engine_superuser()

    with Session(engine) as session:

        session.add_all(list_data)
        session.commit()


if __name__ == "__main__":
    user = [
        paul,
        jean,
        george,
        michel
        ]

    client = [
        bowling_cie,
        staple_hero,
    ]

    # contrat_data = [
    #     contrat_bowling,
    #     contrat_staple,
    # ]

    # event_data = [
    #     drink,
    # ]

    _add_all(user)
    print("job done !")
