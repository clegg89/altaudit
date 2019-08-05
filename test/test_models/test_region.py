"""Unit Tests for Region model"""
import pytest

from altaudit.models import Region

def test_create_region_table(db):
    assert db.has_table('regions')

def test_add_region(db_session):
    us = Region(name='US')
    db_session.add(us)

    assert us == db_session.query(Region).filter(Region.name=='US').first()

    db_session.delete(us)
