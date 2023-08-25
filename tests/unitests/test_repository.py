from sqlalchemy.orm import sessionmaker
import pytest

from models import Base, User, Client, Contrat, Evenement, Departements, ContratStatus
from setup import _create_test_engine


@pytest.fixture
def user_paul():
    _user = User(
                name="paul",
                forname="test",
                email="paul@test1.com",
                departement=Departements.COMMERCIAL,
                )
    return _user


@pytest.fixture
def user_george():
    _user = User(
                name="george",
                forname="test",
                email="george@test2.com",
                departement=Departements.GESTION,
                )
    return _user


@pytest.fixture()
def database_access():
    engine = _create_test_engine()
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    yield session

    session.rollback()
    Base.metadata.drop_all(engine)
    print("fini")


def test_create_user(database_access, user_paul):
    session = database_access
    session.add(user_paul)
    session.commit()

    paul = session.query(User).filter_by(email="paul@test1.com").first()
    print(paul)
    assert paul.name == "paul"
    assert paul.forname == "test"
    assert paul.departement.value == "Commercial", print(paul.departement)


def test_create_user_2(database_access, user_george):
    session = database_access
    session.add(user_george)
    session.commit()

    george = session.query(User).filter_by(email="george@test2.com").first()
    print(george)
    assert george.name == "george"
    assert george.forname == "test"
    assert george.departement.value == "Gestion", print(george.departement)
