"""Unit Tests for the Character Model"""
import pytest

from sqlalchemy.exc import IntegrityError

from altaudit.models import Faction, Class, Race, Region, Realm, Character

def test_create_character_table(db):
    assert db.has_table('characters')

def test_add_character(db_session):
    clegg = Character(name='clegg')

    db_session.add(clegg)

    assert clegg == db_session.query(Character).filter_by(name='clegg').first()

def test_add_realm_character(db_session):
    kj = Realm('kiljaeden')
    clegg = Character(name="clegg")

    kj.characters.append(clegg)

    db_session.add(kj)

    assert clegg == db_session.query(Character).filter_by(name="clegg").join(Realm).filter_by(name="kiljaeden").first()

def test_add_character_realm(db_session):
    clegg = Character(name='clegg')
    kj = Realm('kiljaeden')

    clegg.realm = kj

    db_session.add(clegg)

    assert kj == db_session.query(Realm).filter_by(name="kiljaeden").join(Character).filter_by(name="clegg").first()

def test_character_realm_region(db_session):
    us = Region('us')
    kj = Realm('kiljaeden', us)
    clegg = Character('clegg', realm=kj)

    assert clegg.region_name == 'us'

def test_no_duplicate_characters(db_session):
    us = Region('us')
    kj = Realm('kiljaeden', us)
    clegg = Character('clegg', realm=kj)
    oclegg = Character('clegg', realm=kj)

    db_session.add(clegg)
    db_session.add(oclegg)
    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

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

def test_delete_region_cascade_characters(db_session):
    us = Region('us')
    eu = Region('eu')

    db_session.add(us)
    db_session.add(eu)

    kj = Realm('kiljaeden', us)
    lb = Realm('lightbringer', us)
    ad = Realm('argentdawn', eu)

    clegg = Character('clegg', realm=kj)
    tali = Character('tali', realm=ad)

    db_session.commit()

    db_session.delete(us)

    assert [tali] == db_session.query(Character).all()
