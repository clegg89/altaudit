"""Unit Tests for all models"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from charfetch.models import Base, Class, Region, Realm, Character, Year, Week, Snapshot

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
    session.commit()
    session.close()

def test_create_class_table(db):
    assert db.has_table('classes')

def test_create_region_table(db):
    assert db.has_table('regions')

def test_create_realm_table(db):
    assert db.has_table('realms')

def test_create_character_table(db):
    assert db.has_table('characters')

def test_create_class(db_session):
    warlock = Class('Warlock')

    db_session.add(warlock)

    assert warlock == db_session.query(Class).filter_by(name='Warlock').first()

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

def test_character_realm_region(db_session):
    us = Region('us')
    kj = Realm("Kil'jaeden", 'kiljaeden', us)
    clegg = Character('clegg', realm=kj)

    assert clegg.region_name == 'us'

def test_add_character_class(db_session):
    clegg = Character('clegg', character_class=Class('Warlock'))

    db_session.add(clegg)

    print(db_session.query(Class).all())
    assert "Warlock" == db_session.query(Class).filter_by(name="Warlock").first().name

def test_add_character_class_back_populate(db_session):
    wl = Class('Warlock')
    clegg = Character('clegg', character_class=wl)

    db_session.add(clegg)

    lookup = db_session.query(Class).filter_by(name="Warlock").first()
    lookup.name = 'Warrior'

    assert clegg.character_class.name == 'Warrior'

def test_add_character_constructor(db_session):
    clegg = Character('clegg', level=120)

    db_session.add(clegg)

    assert db_session.query(Character).filter_by(name="clegg").filter_by(level=120).first()


def test_add_snapshots_to_character(db_session):
    clegg = Character(name='clegg')
    s1 = Snapshot()
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][3] = s1

    db_session.add(clegg)

    assert s1 == db_session.query(Snapshot)\
                                .join(Week).filter_by(week=3)\
                                .join(Year).filter_by(year=2019)\
                                .join(Character).filter_by(name='clegg').first()
