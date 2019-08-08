"""Unit Tests for the Gem model"""
import pytest

from altaudit.models import Gem

def test_create_gem_table(db):
    assert db.has_table('gems')

def test_add_gem(db_session):
    quick_sand = Gem(168641, 5, 'Quick Sand Spinel', 'inv_misc_gem_x4_uncommon_perfectcut_yellow', '+50 Haste')

    db_session.add(quick_sand)

    assert quick_sand == db_session.query(Gem).filter_by(id=168641).first()
