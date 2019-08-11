"""Unit tests for Azerite info"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Class, Character, AzeriteTrait

import altaudit.sections as Section

hoa_item_info = {'id': 158075, 'name': 'Heart of Azeroth', 'icon': 'inv_heartofazeroth', 'quality': 6, 'itemLevel': 427, 'azeriteItem': {'azeriteLevel': 47, 'azeriteExperience': 1062, 'azeriteExperienceRemaining': 22815}}

non_hoa_neck_item_info = {'id': 122666, 'name': 'Eternal Woven Ivy Necklace', 'icon': 'inv_misc_herb_15', 'quality': 7, 'itemLevel': 65}

fake_azerite_item_class_powers_in_db = {
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

fake_azerite_item_class_powers_not_in_db = {
    '9': [
        {'id': 561, 'tier': 3, 'spellId': 288802},
        {'id': 124, 'tier': 3, 'spellId': 272891},
        {'id': 132, 'tier': 3, 'spellId': 272944},
        {'id': 133, 'tier': 3, 'spellId': 287637},
        {'id': 33, 'tier': 2, 'spellId': 266180},
        {'id': 465, 'tier': 2, 'spellId': 279926},
        {'id': 22, 'tier': 2, 'spellId': 263984},
        {'id': 209, 'tier': 1, 'spellId': 274418},
        {'id': 16, 'tier': 1, 'spellId': 263962},
        {'id': 19, 'tier': 0, 'spellId': 263978},
        {'id': 238, 'tier': 4, 'spellId': 275372},
        {'id': 185, 'tier': 4, 'spellId': 273521},
        {'id': 239, 'tier': 4, 'spellId': 275395},
        {'id': 192, 'tier': 4, 'spellId': 273523},
        {'id': 234, 'tier': 4, 'spellId': 275425},
        {'id': 463, 'tier': 4, 'spellId': 279909}]}

fake_azerite_item_traits_in_db = {
        'id' : 165822,
        'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 13, 'tier': 0, 'spellId': 263978},
                 {'id': 15, 'tier': 1, 'spellId': 263962},
                 {'id': 30, 'tier': 2, 'spellId': 266180},
                 {'id': 123, 'tier': 3, 'spellId': 272891},
                 {'id': 183, 'tier': 4, 'spellId': 273521}]}}

fake_azerite_item_traits_not_in_db = {
        'id' : 165822,
        'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 19, 'tier': 0, 'spellId': 263978},
                 {'id': 16, 'tier': 1, 'spellId': 263962},
                 {'id': 33, 'tier': 2, 'spellId': 266180},
                 {'id': 124, 'tier': 3, 'spellId': 272891},
                 {'id': 185, 'tier': 4, 'spellId': 273521}]}}

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add(Class('Warlock', id=9))

    for trait in fake_azerite_item_class_powers_in_db['9']:
        session.add(AzeriteTrait(trait['id'], trait['spellId'],
            'Fake Azerite Name', 'inv_fake_icon'))

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
    mock = mocker.MagicMock()

    mock.get_item.return_value = { 'azeriteClassPowers' :
            fake_azerite_item_class_powers_in_db }

    return mock

def test_hoa_info():
    jack = Character('jack')
    response = { 'items' : { 'neck' : hoa_item_info } }
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == 47
    assert jack.azerite_experience == 1062
    assert jack.azerite_experience_remaining == 22815

def test_hoa_info_no_neck():
    jack = Character('jack')
    response = { 'items' : {} }
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_experience == None
    assert jack.azerite_experience_remaining ==  None

def test_hoa_info_non_hoa_neck():
    jack = Character('jack')
    response = { 'items' : { 'neck' : non_hoa_neck_item_info } }
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_experience == None
    assert jack.azerite_experience_remaining ==  None

def test_azerite_item_in_db(db_session, mock_api):
    jack = Character('jack', class_id=9)
    response = { 'items' : { 'head' : fake_azerite_item_traits_in_db } }
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Fake Azerite Name'
    assert jack._head_tier0_selected.icon == 'inv_fake_icon'
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Fake Azerite Name'
    assert jack._head_tier0_available[0].icon == 'inv_fake_icon'
    assert len(jack._head_tier0_available) == 1

def test_azerite_item_not_in_db(db_session, mock_api):
    mock_api.get_item.return_value = { 'azeriteClassPowers' :
            fake_azerite_item_class_powers_not_in_db }

    def _get_spell(region, spellId, locale=None):
        assert region == 'us'
        assert locale == 'en_US'
        return { 'id' : spellId, 'name' : 'Fake Name', 'icon' : 'inv_fake' }

    mock_api.get_spell.side_effect = _get_spell

    jack = Character('jack', class_id=9)
    response = { 'items' : { 'head' : fake_azerite_item_traits_not_in_db } }
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 19
    assert mock_api.get_spell.call_count == 16
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Fake Name'
    assert jack._head_tier0_selected.icon == 'inv_fake'
    assert jack._head_tier0_available[0].id == 19
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Fake Name'
    assert jack._head_tier0_available[0].icon == 'inv_fake'

def test_azerite_item_no_item():
    jack = Character('jack')
    response = { 'items' : {} }

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []

def test_azerite_item_no_traits():
    jack = Character('jack')
    response = { 'items' : { 'head' : { 'id' : 165822, 'azeriteEmpoweredItem' : { 'azeritePowers' : [] } } } }

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []
