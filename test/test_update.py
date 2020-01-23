"""Unit Tests for altaudit.update"""
import pytest

import copy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import altaudit.update as updater
from altaudit.models import Base, Region, Realm, Character

@pytest.fixture
def db():
    us = Region(name='us')
    kj = Realm(name='kiljaeden', region=us)
    lb = Realm(name='lightbringer', region=us)
    archer = Character(name='archer', realm=kj, lastmodified=123456)
    rando = Character(name='rando', realm=kj, lastmodified=7891011)
    ray = Character(name='ray', realm=lb, lastmodified=13141516)

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()
    session.add_all([archer, rando, ray])
    session.commit()
    session.close()

    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    Session = sessionmaker(db)
    session = Session()
    yield session
    session.close()

def test_update_config_no_change():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando', 'randy'] } }
    expected = copy.deepcopy(config)
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_name():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando', 'randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'][0] = 'ray'
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['name'] = 'ray'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_existing():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'].append('archer')
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_new():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'] = ['archer']
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_remove_empty():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    del expected['us']['lightbringer']
    expected['us']['kiljaeden'].append('randy')
    charIn = { 'name' : 'randy', 'realm' : 'lightbringer' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'kiljaeden'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_name_and_realm():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'].append('ray')
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'
    charOut['name'] = 'ray'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_db_no_change(db_session):
    updater._update_db(db_session, 'us',
            { 'name' : 'archer', 'realm' : 'kiljaeden' },
            { 'name' : 'archer', 'realm' : 'kiljaeden' })
    db_session.commit()

    charQuery = db_session.query(Character).filter_by(name='archer')
    archer = charQuery.first()

    assert charQuery.count() == 1
    assert archer.realm_slug == 'kiljaeden'
    assert archer.realm.region_name == 'us'
    assert archer.lastmodified == 123456

def test_update_db_change_name(db_session):
    updater._update_db(db_session, 'us',
            { 'name' : 'archer', 'realm' : 'kiljaeden' },
            { 'name' : 'jack', 'realm' : 'kiljaeden' })
    db_session.commit()

    charQuery = db_session.query(Character).filter_by(name='jack')
    jack = charQuery.first()

    assert charQuery.count() == 1
    assert jack.realm_slug == 'kiljaeden'
    assert jack.realm.region_name == 'us'
    assert jack.lastmodified == 123456
    assert db_session.query(Character).filter_by(name='archer').count() == 0

def test_update_db_change_realm_existing(db_session):
    updater._update_db(db_session, 'us',
            { 'name' : 'archer', 'realm' : 'kiljaeden' },
            { 'name' : 'archer', 'realm' : 'lightbringer' })
    db_session.commit()

    charQuery = db_session.query(Character).filter_by(name='archer')
    archer = charQuery.first()

    assert charQuery.count() == 1
    assert archer.realm_slug == 'lightbringer'
    assert archer.realm.region_name == 'us'
    assert archer.lastmodified == 123456

def test_update_db_change_realm_new(db_session):
    updater._update_db(db_session, 'us',
            { 'name' : 'archer', 'realm' : 'kiljaeden' },
            { 'name' : 'archer', 'realm' : 'illidan' })
    db_session.commit()

    charQuery = db_session.query(Character).filter_by(name='archer')
    archer = charQuery.first()

    assert charQuery.count() == 1
    assert archer.realm_slug == 'illidan'
    assert archer.realm.region_name == 'us'
    assert archer.lastmodified == 123456

def test_update_db_change_name_and_realm(db_session):
    updater._update_db(db_session, 'us',
            { 'name' : 'archer', 'realm' : 'kiljaeden' },
            { 'name' : 'jack', 'realm' : 'lightbringer' })
    db_session.commit()

    charQuery = db_session.query(Character).filter_by(name='jack')
    jack = charQuery.first()

    assert charQuery.count() == 1
    assert jack.realm_slug == 'lightbringer'
    assert jack.realm.region_name == 'us'
    assert jack.lastmodified == 123456
    assert db_session.query(Character).filter_by(name='archer').count() == 0
