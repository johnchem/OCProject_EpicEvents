from models import Base, User, Client, Contrat, Evenement, Departements, ContratStatus
from conftest import *

# --------- Test Object CRUD : User -------------


def test_create_user(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.commit()

    paul = session.query(User).filter_by(email="paul@test1.com").first()
    print(paul)
    assert paul.name == "paul"
    assert paul.forname == "test"
    assert paul.departement.value == "Commercial", print(paul.departement)

# --------- Test Object CRUD : Client -------------


def test_create_client(database_access, client_bowling):
    session = database_access
    print(client_bowling)
    session.add(client_bowling)
    session.commit()

    client = session.query(Client).filter_by(full_name="roule maboule").first()
    assert client.full_name == "roule maboule"
    assert client.email == "rmaboule@bowling.com"
    assert client.phone == "0123456789"
    assert client.company_name == "Bowling & Cie"
    assert client.commercial_contact.email == "paul@test1.com"

# --------- Test Object CRUD : Contract -----------


def test_create_contrat(database_access, contrat_roule_maboule):
    session = database_access
    session.add(contrat_roule_maboule)
    session.commit()

    contrat = session.query(Contrat).filter_by(full_name="roule maboule").first()
    assert contrat.client.full_name == "roule maboule"
    assert contrat.total_amount == 10000
    assert contrat.remaining_amount == 250
    assert contrat.contrat_status == ContratStatus.SIGNED

# --------- Test Object CRUD : Evenement ----------

# --------- Test General function -------------

def test_add_multiple_object():
    # test add_bulk
    pass
