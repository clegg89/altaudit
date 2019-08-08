"""Unit tests for Azerite info"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, AzeriteTrait

import altaudit.sections as Section

fake_azerite_item_class_powers = {
    '5': [
        {'id': 560, 'tier': 3, 'spellId': 288802},
        {'id': 113, 'tier': 3, 'spellId': 272775},
        {'id': 114, 'tier': 3, 'spellId': 272780},
        {'id': 115, 'tier': 3, 'spellId': 272788},
        {'id': 30, 'tier': 2, 'spellId': 266180},
        {'id': 102, 'tier': 2, 'spellId': 267892},
        {'id': 42, 'tier': 2, 'spellId': 267883},
        {'id': 204, 'tier': 1, 'spellId': 274366},
        {'id': 15, 'tier': 1, 'spellId': 263962},
        {'id': 13, 'tier': 0, 'spellId': 263978},
        {'id': 227, 'tier': 4, 'spellId': 275541},
        {'id': 164, 'tier': 4, 'spellId': 273307},
        {'id': 228, 'tier': 4, 'spellId': 275602},
        {'id': 165, 'tier': 4, 'spellId': 273313},
        {'id': 236, 'tier': 4, 'spellId': 275722},
        {'id': 166, 'tier': 4, 'spellId': 288340}],
    '8': [
        {'id': 560, 'tier': 3, 'spellId': 288802},
        {'id': 127, 'tier': 3, 'spellId': 286027},
        {'id': 128, 'tier': 3, 'spellId': 272932},
        {'id': 132, 'tier': 3, 'spellId': 272968},
        {'id': 30, 'tier': 2, 'spellId': 266180},
        {'id': 461, 'tier': 2, 'spellId': 279926},
        {'id': 21, 'tier': 2, 'spellId': 263984},
        {'id': 205, 'tier': 1, 'spellId': 274379},
        {'id': 15, 'tier': 1, 'spellId': 263962},
        {'id': 13, 'tier': 0, 'spellId': 263978},
        {'id': 214, 'tier': 4, 'spellId': 274594},
        {'id': 167, 'tier': 4, 'spellId': 273326},
        {'id': 215, 'tier': 4, 'spellId': 274596},
        {'id': 168, 'tier': 4, 'spellId': 288755},
        {'id': 225, 'tier': 4, 'spellId': 279854},
        {'id': 170, 'tier': 4, 'spellId': 288164}],
    '9': [
        {'id': 560, 'tier': 3, 'spellId': 288802},
        {'id': 123, 'tier': 3, 'spellId': 272891},
        {'id': 130, 'tier': 3, 'spellId': 272944},
        {'id': 131, 'tier': 3, 'spellId': 287637},
        {'id': 30, 'tier': 2, 'spellId': 266180},
        {'id': 461, 'tier': 2, 'spellId': 279926},
        {'id': 21, 'tier': 2, 'spellId': 263984},
        {'id': 208, 'tier': 1, 'spellId': 274418},
        {'id': 15, 'tier': 1, 'spellId': 263962},
        {'id': 13, 'tier': 0, 'spellId': 263978},
        {'id': 230, 'tier': 4, 'spellId': 275372},
        {'id': 183, 'tier': 4, 'spellId': 273521},
        {'id': 231, 'tier': 4, 'spellId': 275395},
        {'id': 190, 'tier': 4, 'spellId': 273523},
        {'id': 232, 'tier': 4, 'spellId': 275425},
        {'id': 460, 'tier': 4, 'spellId': 279909}]}

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    # TODO add some AzeriteTrait models here

    session.commit()
    session.close()

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    session = sessionmaker(db)()
    yield session
    session.close()

@pytest.fixture
def mock_api(mocker):
    return mocker.MagicMock()

"""
Tests:
    - hoa info with valid HOA (no azerite pieces to save exec time)
    - hoa info None with no HOA (no azerite pieces to save exec time)
    - Valid Selected and Available traits for single AP slot
    - Valid Selected and Available traits for all AP slot
    - Traits filled in from database when present (use single AP slot)
    - Traits fetched from API when not present (use single AP slot)
    - Traits are None and empty when no slot
"""
