"""Unit Tests for the AzeriteTrait model"""
import pytest

from altaudit.models import AzeriteTrait

def test_create_azerite_trait_table(db):
    assert db.has_table('azerite_traits')

def test_add_azerite_trait(db_session):
    empowered = AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard')

    db_session.add(empowered)

    assert empowered == db_session.query(AzeriteTrait).filter(AzeriteTrait.id==13).first()

    db_session.delete(empowered)

def test_azerite_trait_string():
    empowered = AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard')

    assert str(empowered) == '13+263978+Azerite Empowered+inv_smallazeriteshard'
