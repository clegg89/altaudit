"""Unit tests for Azerite info"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, AzeriteTrait

import altaudit.sections as Section

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    # TODO add some AzeriteTrait models here

    session.commit()
    session.close()

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    session = sessionmaker(db)()
    yield session
    session.close()
