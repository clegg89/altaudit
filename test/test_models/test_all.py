"""Unit Tests for all models"""
import pytest

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from charfetch.models import Base, Region, Realm

@pytest.fixture
def db():
    path = os.path.dirname(os.path.realpath(__file__))
    engine = create_engine("sqlite:///{}/test.db".format(path))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    Session = sessionmaker(db)
    session = Session()
    yield session
    session.commit()
    session.close()

def test_create_region_table(db):
    assert db.has_table('regions')

def test_create_realm_table(db):
    assert db.has_table('realms')

def test_create_character_table(db):
    assert db.has_table('characters')

def test_add_region(db_session):
    us = Region(name='US')
    db_session.add(us)

    assert us == db_session.query(Region).filter(Region.name=='US').first()

    db_session.delete(us)

def test_add_region_realm(db_session):
    us = Region(name='US')
    kj = Realm(name="Kil'jaeden", slug='kiljaeden')

    us.realms.append(kj)

    db_session.add(us)

    assert kj == db_session.query(Realm).filter_by(name="Kil'jaeden").join(Region).filter_by(name='US').first()

def test_add_realm(db_session):
    kj = Realm(name="Kil'jaeden", slug='kiljaeden')
    db_session.add(kj)

    assert kj == db_session.query(Realm).filter_by(name="Kil'jaeden").filter_by(slug='kiljaeden').first()

def test_add_realm_region(db_session):
    kj = Realm(name="Kil'jaeden", slug='kiljaeden')
    us = Region(name='US')

    kj.region = us

    db_session.add(kj)

    assert us == db_session.query(Region).filter_by(name='US').join(Realm).filter_by(name="Kil'jaeden").first()
