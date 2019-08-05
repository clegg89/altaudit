"""Unit Tests for Game Data models"""
import pytest

from altaudit.models import Faction, Class, Race

def test_create_class_table(db):
    assert db.has_table('classes')

def test_create_faction_table(db):
    assert db.has_table('factions')

def test_create_race_table(db):
    assert db.has_table('races')

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
