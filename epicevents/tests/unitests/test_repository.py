import pytest
from datetime import datetime
import sqlalchemy

from conftest import *
from conftest import DT_STRING
from werkzeug.security import check_password_hash
from epicevents.backend.models import User, Client, Contract, Evenement, Departements, ContractStatus
from epicevents.backend.repository import SqlAlchemyRepository

# --------- Test Object CRUD : User -------------


def test_create_user(database_access, user_paul):
    session = database_access

    repository = SqlAlchemyRepository(session)
    repository.add(user_paul)
    repository.commit()

    paul = session.query(User).filter_by(email="paul@test1.com").first()

    assert paul.name == "paul"
    assert paul.forname == "test"
    assert paul.departement.value == "Commercial", print(paul.departement)


def test_get_user(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.commit()

    repository = SqlAlchemyRepository(session)
    paul = repository.get_user("paul@test1.com")

    assert paul.name == "paul"
    assert paul.forname == "test"
    assert paul.departement.value == "Commercial", print(paul.departement)


def test_list_user(database_access, user_paul, user_george, user_michel, user_jean):
    session = database_access
    session.add(user_paul)
    session.add(user_george)
    session.add(user_michel)
    session.add(user_jean)
    session.commit()

    repository = SqlAlchemyRepository(session)
    list_user = repository.list_user()

    assert len(list_user) == 4
    assert "paul" in [x.name for x in list_user]
    assert "george" in [x.name for x in list_user]
    assert "michel" in [x.name for x in list_user]
    assert "jean" in [x.name for x in list_user]
    assert ["paul", "jean"] == [x.name for x in list_user if x.departement == Departements.COMMERCIAL]


def test_update_user(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.flush()
    session.refresh(user_paul)

    repository = SqlAlchemyRepository(session)
    user_generator = repository.update_user(user_paul.id)
    paul = next(user_generator)
    paul.name = "jean-michel"
    paul.forname = "update"
    paul.departement = Departements.SUPPORT
    try:
        next(user_generator)
    except StopIteration:
        pass

    paul_control = session.query(User).filter_by(email="paul@test1.com").first()

    assert paul_control.name == "jean-michel"
    assert paul_control.forname == "update"
    assert paul_control.departement == Departements.SUPPORT


def test_delete_user(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.flush()
    session.refresh(user_paul)

    repository = SqlAlchemyRepository(session)
    repository.delete_user(user_paul.id)
    session.commit()
    with pytest.raises(sqlalchemy.exc.NoResultFound, match="No row was found when one was required"):
        session.query(User).where(User.id == user_paul.id).one()


# --------- Test Object CRUD : Client -------------


def test_create_client(database_access, client_bowling):
    session = database_access
    repository = SqlAlchemyRepository(session)
    repository.add(client_bowling)
    session.commit()

    client = session.query(Client).filter_by(full_name="roule maboule").first()
    assert client.full_name == "roule maboule"
    assert client.email == "rmaboule@bowling.com"
    assert client.phone == "0123456789"
    assert client.company_name == "Bowling & Cie"
    assert client.commercial_contact.email == "paul@test1.com"


def test_list_client(database_access, client_bowling, client_bowling_2, client_staplehero):
    session = database_access
    session.add(client_bowling)
    session.add(client_bowling_2)
    session.add(client_staplehero)
    session.flush()

    repository = SqlAlchemyRepository(session)
    list_client = repository.list_client()

    assert len(list_client) == 3
    assert "roule maboule" in [x.full_name for x in list_client]
    assert "rouli bouli" in [x.full_name for x in list_client]
    assert "jean nemarre" in [x.full_name for x in list_client]
    assert ["roule maboule", "rouli bouli"].sort() == [
        x.full_name for x in list_client if x.company_name == "Bowling & Cie"
    ].sort()


def test_update_client(database_access, client_bowling, user_george):
    session = database_access
    session.add(user_george)
    session.add(client_bowling)
    session.commit()
    session.refresh(user_george)
    session.refresh(client_bowling)

    repository = SqlAlchemyRepository(session)
    client_generator = repository.update_client(client_bowling.id)
    bowling = next(client_generator)
    bowling.full_name = "rolli pauli"
    bowling.phone = "9876543210"
    bowling.commercial_contact = user_george
    try:
        next(client_generator)
    except StopIteration:
        pass

    bowling_control = session.query(Client).filter_by(email="rmaboule@bowling.com").first()
    assert bowling_control.full_name == "rolli pauli"
    assert bowling_control.phone == "9876543210"
    assert bowling_control.company_name == "Bowling & Cie"
    assert bowling_control.commercial_contact.email == "george@test2.com"


def test_delete_client(database_access, client_bowling):
    session = database_access
    session.add(client_bowling)
    session.flush()
    session.refresh(client_bowling)

    repository = SqlAlchemyRepository(session)
    repository.delete_client(client_bowling.id)
    session.commit()
    with pytest.raises(sqlalchemy.exc.NoResultFound, match="No row was found when one was required"):
        session.query(Client).where(Client.id == client_bowling.id).one()


# --------- Test Object CRUD : Contract -----------


def test_create_contract(database_access, contract_roule_maboule):
    session = database_access
    repository = SqlAlchemyRepository(session)
    repository.add(contract_roule_maboule)
    session.commit()

    contract = session.query(Contract).join(Client).filter(Client.full_name == "roule maboule").first()
    assert contract.client.full_name == "roule maboule"
    assert contract.total_amount == 10000
    assert contract.remaining_amount == 250
    assert contract.contract_status == ContractStatus.SIGNED


def test_list_contract(database_access, contract_jean_nemarre, contract_roule_maboule):
    session = database_access
    session.add(contract_jean_nemarre)
    session.add(contract_roule_maboule)
    session.flush()

    repository = SqlAlchemyRepository(session)
    list_contract = repository.list_contract()

    assert 2 == len(list_contract)
    assert 35000 == sum([x.total_amount for x in list_contract])
    assert 2 == len([x for x in list_contract if x.client.company_name == "Bowling & Cie"])


def test_update_contract(database_access, contract_roule_maboule):
    session = database_access
    session.add(contract_roule_maboule)
    session.commit()
    session.refresh(contract_roule_maboule)

    repository = SqlAlchemyRepository(session)
    contract_generator = repository.update_contract(contract_roule_maboule.id)
    contract = next(contract_generator)
    contract.total_amount = 1500
    contract.remaining_amount = 0
    contract.contract_status = ContractStatus.NOT_SIGNED
    try:
        next(contract_generator)
    except StopIteration:
        pass

    contract_control = session.query(Contract).join(Client).where(Client.email == "rmaboule@bowling.com").first()
    assert contract_control.total_amount == 1500
    assert contract_control.remaining_amount == 0
    assert contract_control.contract_status == ContractStatus.NOT_SIGNED


def test_delete_contract(database_access, contract_roule_maboule):
    session = database_access
    session.add(contract_roule_maboule)
    session.flush()
    session.refresh(contract_roule_maboule)

    repository = SqlAlchemyRepository(session)
    repository.delete_contract(contract_roule_maboule.id)
    session.commit()
    with pytest.raises(sqlalchemy.exc.NoResultFound, match="No row was found when one was required"):
        session.query(Contract).where(Contract.id == contract_roule_maboule.id).one()


# --------- Test Object CRUD : Evenement ----------


def test_create_evenement(database_access, evenement_contract_roule_maboule):
    session = database_access
    session.add(evenement_contract_roule_maboule)
    session.commit()

    event = session.query(Evenement).join(Client).filter(Client.full_name == "roule maboule").first()
    assert event.client.full_name == "roule maboule"
    assert event.contract.client.full_name == "roule maboule"
    assert event.event_date_start == datetime.strptime("01/05/2025 10:25:00", DT_STRING)
    assert event.event_date_end == datetime.strptime("06/05/2025 10:25:00", DT_STRING)
    assert event.location == "bali-bali"
    assert event.attendees == 10
    assert event.contact_support.name == "michel"
    assert event.note == "les chefs se la coule douce"


# --------- Test User Authentification --------


def test_change_password(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.flush()
    session.refresh(user_paul)

    paul = session.query(User).where(User.email == "paul@test1.com").first()
    paul.password = "testpassword"

    assert paul.password != "testpassword"
    assert check_password_hash(paul.password, "testpassword")


def test_log_in(database_access, user_paul):
    session = database_access
    session.add(user_paul)

    repository = SqlAlchemyRepository(session)
    response = repository.user_login("paul@test1.com", "abc123!")
    session.commit()

    assert response
    assert repository.user_auth


def test_logout(database_access):
    session = database_access
    repository = SqlAlchemyRepository(session)
    response = repository.user_logout()

    assert response
    assert repository.user_auth is False


# --------- Test General function -------------
