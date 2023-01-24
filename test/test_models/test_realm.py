"""Unit Tests for Realm model"""
import pytest

from altaudit.models import Region, Realm

from sqlalchemy.inspection import inspect

def test_create_realm_table(db):
    assert inspect(db).has_table('realms')

def test_add_realm(db_session):
    kj = Realm('kiljaeden')
    db_session.add(kj)

    assert kj == db_session.query(Realm).filter_by(name='kiljaeden').first()

def test_add_region_realm(db_session):
    us = Region(name='US')
    kj = Realm('kiljaeden')

    us.realms.append(kj)

    db_session.add(us)

    assert kj == db_session.query(Realm).filter_by(name="kiljaeden").join(Region).filter_by(name='US').first()

def test_add_realm_region(db_session):
    kj = Realm('kiljaeden')
    us = Region(name='US')

    kj.region = us

    db_session.add(kj)
    assert us == db_session.query(Region).filter_by(name='US').join(Realm).filter_by(name="kiljaeden").first()

def test_no_duplicate_realms(db_session_integrityerror):
    us = Region('us')
    kj = Realm('kiljaeden', us)
    okj = Realm('kiljaeden', us)

    db_session_integrityerror.add(kj)
    db_session_integrityerror.add(okj)

def test_delete_region_cascade_realms(db_session):
    us = Region('us')
    eu = Region('eu')

    db_session.add(us)
    db_session.add(eu)

    kj = Realm('kiljaeden', us)
    lb = Realm('lightbringer', us)
    ad = Realm('argentdawn', eu)

    db_session.commit()

    db_session.delete(us)

    assert [ad] == db_session.query(Realm).all()
