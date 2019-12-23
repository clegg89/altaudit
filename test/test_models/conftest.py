"""Common fixtures for Model unit tests"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from altaudit.models import Base

@pytest.fixture
def db():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    Session = sessionmaker(db)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def db_session_integrityerror(db_session):
    yield db_session
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
