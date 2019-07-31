"""Unit Tests for all models"""
import pytest

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from charfetch.models import Base, Region, Realm, Character

@pytest.fixture
def db():
    path = os.path.dirname(os.path.realpath(__file__))
    db_path = '{}/test.db'.format(path)
    engine = create_engine("sqlite:///{}".format(db_path))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    os.remove(db_path)

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

def test_add_realm_character(db_session):
    kj = Realm(name="Kil'jaeden", slug='kiljaeden')
    clegg = Character(name="clegg")

    kj.characters.append(clegg)

    db_session.add(kj)

    assert clegg == db_session.query(Character).filter_by(name="clegg").join(Realm).filter_by(name="Kil'jaeden").first()

def test_add_character(db_session):
    clegg = Character(name='clegg')

    db_session.add(clegg)

    assert clegg == db_session.query(Character).filter_by(name='clegg').first()

def test_add_character_realm(db_session):
    clegg = Character(name='clegg')
    kj = Realm(name="Kil'jaeden", slug='kiljaeden')

    clegg.realm = kj

    db_session.add(clegg)

    assert kj == db_session.query(Realm).filter_by(name="Kil'jaeden").join(Character).filter_by(name="clegg").first()
