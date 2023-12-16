import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from epicevents.setup import _create_test_engine
from epicevents.backend.models import Base, User, Client, Contract, Evenement, Departements, ContractStatus

DT_STRING = "%d/%m/%Y %H:%M:%S"

# ---------- General Tooling -------------


@pytest.fixture
def create_object_record(_session_creation):
    def _create_object_record(obj):
        session = _session_creation
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj

    return _create_object_record


@pytest.fixture()
def _session_creation():
    engine = _create_test_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@pytest.fixture()
def database_access():
    engine = _create_test_engine()
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()

    yield session

    session.rollback()
    Base.metadata.drop_all(engine)


# -------------- User Object ----------------


@pytest.fixture
def user_paul():
    _user = User(
        name="paul",
        forname="test",
        email="paul@test1.com",
        password="abc123!",
        departement=Departements.COMMERCIAL,
    )
    return _user


@pytest.fixture
def user_jean():
    _user = User(
        name="jean",
        forname="test",
        email="jean@test1.com",
        password="abc123!",
        departement=Departements.COMMERCIAL,
    )
    return _user


@pytest.fixture
def user_george():
    _user = User(
        name="george",
        forname="test",
        email="george@test2.com",
        password="abc123!",
        departement=Departements.GESTION,
    )
    return _user


@pytest.fixture
def user_michel():
    _user = User(
        name="michel", forname="test", email="michel@test3.com", password="abc123!", departement=Departements.SUPPORT
    )
    return _user


# ---------- Client Object --------------


@pytest.fixture
def client_bowling(create_object_record, user_paul):
    user_paul = create_object_record(user_paul)

    _client = Client(
        full_name="roule maboule",
        email="rmaboule@bowling.com",
        phone="0123456789",
        company_name="Bowling & Cie",
        commercial_contact=user_paul,
    )
    return _client


@pytest.fixture
def client_bowling_2(create_object_record, user_jean):
    user_jean = create_object_record(user_jean)

    _client = Client(
        full_name="rouli bouli",
        email="rbouli@bowling.com",
        phone="0123456789",
        company_name="Bowling & Cie",
        commercial_contact=user_jean,
    )
    return _client


@pytest.fixture
def client_staplehero(create_object_record, user_paul):
    user_paul = create_object_record(user_paul)

    _client = Client(
        full_name="jean nemarre",
        email="jnemarre@staplehero.com",
        phone="0123456789",
        company_name="StapleHero",
        commercial_contact=user_paul,
    )
    return _client


# ---------- Contract Object --------------


@pytest.fixture
def contract_roule_maboule(create_object_record, client_bowling):
    client_bowling = create_object_record(client_bowling)

    _contract = Contract(
        client=client_bowling, total_amount=10000, remaining_amount=250, contract_status=ContractStatus.SIGNED
    )
    return _contract


@pytest.fixture
def contract_jean_nemarre(create_object_record, client_bowling_2):
    client_bowling = create_object_record(client_bowling_2)

    _contract = Contract(
        client=client_bowling,
        total_amount=25000,
        remaining_amount=25000,
        contract_status=ContractStatus.NOT_SIGNED,
    )
    return _contract


# ---------- Evenement Object --------------


@pytest.fixture
def evenement_contract_roule_maboule(create_object_record, contract_roule_maboule, user_michel):
    user_michel = create_object_record(user_michel)
    contract_roule_maboule = create_object_record(contract_roule_maboule)

    _event = Evenement(
        nom="Steering comitee",
        contract=contract_roule_maboule,
        event_date_start=datetime.strptime("01/05/2025 10:25:00", DT_STRING),
        event_date_end=datetime.strptime("06/05/2025 10:25:00", DT_STRING),
        location="bali-bali",
        attendees=10,
        contact_support=user_michel,
        note="les chefs se la coule douce",
    )
    return _event
