"""Unit Tests for all models"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from charfetch.models import Base, Faction, Class, Race, Region, Realm, Character, Year, Week, Snapshot

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

def test_create_faction_table(db):
    assert db.has_table('factions')

def test_create_race_table(db):
    assert db.has_table('races')

def test_create_region_table(db):
    assert db.has_table('regions')

def test_create_realm_table(db):
    assert db.has_table('realms')

def test_create_character_table(db):
    assert db.has_table('characters')

def test_create_class(db_session):
    warlock = Class('Warlock', id=9)

    db_session.add(warlock)

    assert warlock == db_session.query(Class).filter_by(id=9).first()

def test_create_faction(db_session):
    horde = Faction('horde')

    db_session.add(horde)

    assert horde == db_session.query(Faction).first()

def test_create_race(db_session):
    undead = Race('Undead', id=5)

    db_session.add(undead)

    assert undead == db_session.query(Race).filter_by(id=5).first()

def test_race_faction(db_session):
    horde = Faction('horde', id=1)
    undead = Race('undead', faction=horde)

    db_session.add(horde)
    db_session.add(undead)
    db_session.commit()

    assert 1 == db_session.query(Race).first().faction_id

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

    assert "Warlock" == db_session.query(Class).filter_by(name="Warlock").first().name

def test_character_class_by_id(db_session):
    warlock = Class('Warlock', id=9)

    db_session.add(warlock)

    clegg = Character('clegg', class_id=9)

    db_session.add(clegg)
    db_session.flush()

    assert clegg.class_name == 'Warlock'

def test_add_character_class_back_populate(db_session):
    wl = Class('Warlock')
    clegg = Character('clegg', character_class=wl)

    db_session.add(clegg)

    lookup = db_session.query(Class).filter_by(name="Warlock").first()
    lookup.name = 'Warrior'

    assert clegg.character_class.name == 'Warrior'

def test_character_class_delete_does_not_propogate(db_session):
    wl = Class('warlock', id=9)
    clegg = Character('clegg', character_class=wl)

    db_session.add(wl)
    db_session.add(clegg)
    db_session.commit()
    db_session.close()

    db_session.delete(wl)
    db_session.commit()
    db_session.close()

    assert 9 == db_session.query(Character).first().class_id
    assert None == db_session.query(Character).first().character_class
    assert None == db_session.query(Character).first().class_name

def test_character_class_readd_works(db_session):
    wl = Class('warlock', id=9)
    clegg = Character('clegg', character_class=wl)

    db_session.add(wl)
    db_session.add(clegg)
    db_session.commit()
    db_session.close()

    db_session.delete(wl)
    db_session.commit()
    db_session.close()

    newwl = Class('warlock', id=9)
    db_session.add(newwl)
    db_session.commit()
    db_session.close()

    assert 9 == db_session.query(Character).first().class_id
    assert 'warlock' == db_session.query(Character).first().class_name

def test_character_faction(db_session):
    horde = Faction('horde', id=1)
    clegg = Character('clegg', faction=horde)

    db_session.add(clegg)
    db_session.commit()
    db_session.close()

    assert 'horde' == db_session.query(Character).first().faction_name

def test_add_character_race(db_session):
    clegg = Character('clegg', race=Race('Undead'))

    db_session.add(clegg)

    assert 'Undead' == db_session.query(Race).filter_by(name="Undead").first().name

def test_add_character_constructor(db_session):
    clegg = Character('clegg', level=120)

    db_session.add(clegg)

    assert db_session.query(Character).filter_by(name="clegg").filter_by(level=120).first()


def test_add_snapshots_to_character(db_session):
    clegg = Character(name='clegg')
    s1 = Snapshot()
    s1.world_quests = 10
    s1.dungeons = 20
    s1.azerite_power = 1500
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][3] = s1

    db_session.add(clegg)

    assert s1 == db_session.query(Snapshot)\
                                .join(Week).filter_by(week=3)\
                                .join(Year).filter_by(year=2019)\
                                .join(Character).filter_by(name='clegg').first()

def test_delete_region_cascade_realms(db_session):
    us = Region('us')
    eu = Region('eu')

    db_session.add(us)
    db_session.add(eu)

    kj = Realm("Kil'jaeden", 'kiljaeden', us)
    lb = Realm("Lightbringer", 'lightbringer', us)
    ad = Realm('Argent Dawn', 'argentdawn', eu)

    db_session.commit()

    db_session.delete(us)

    assert [ad] == db_session.query(Realm).all()

def test_delete_region_cascade_characters(db_session):
    us = Region('us')
    eu = Region('eu')

    db_session.add(us)
    db_session.add(eu)

    kj = Realm("Kil'jaeden", 'kiljaeden', us)
    lb = Realm("Lightbringer", 'lightbringer', us)
    ad = Realm('Argent Dawn', 'argentdawn', eu)

    clegg = Character('clegg', realm=kj)
    tali = Character('tali', realm=ad)

    db_session.commit()

    db_session.delete(us)

    assert [tali] == db_session.query(Character).all()
