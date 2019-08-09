"""Unit Test for Audit Info"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, Gem
from altaudit.gem_enchant import gem_lookup

import altaudit.sections as Section

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add_all([Gem(k, v['quality'], v['name'], v['icon'], v['stat'])
        for k,v in gem_lookup.items()])

    session.commit()
    session.close()

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture
def mock_api(mocker):
    mock = mocker.MagicMock()

    return mock

@pytest.fixture
def db_session(db):
    session = sessionmaker(db)()
    yield session
    session.close()

def test_audit_regular_item():
    jack = Character('jack')
    response = { 'items' : {
        'finger1' : { 'tooltipParams' : { 'enchant' : 6109 }}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.finger1_enchant_id == 6109
    assert jack.finger1_enchant_quality == 4
    assert jack.finger1_enchant_name == 'Accord of Haste'
    assert jack.finger1_enchant_description == '+60 Haste'

def test_audit_item_missing():
    jack = Character('jack')
    response = { 'items' : {},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.finger1_enchant_id == None
    assert jack.finger1_enchant_quality == 0
    assert jack.finger1_enchant_name == 'None'
    assert jack.finger1_enchant_description == None

def test_audit_item_no_enchant():
    jack = Character('jack')
    response = { 'items' : {
        'finger1' : { 'tooltipParams' : {}}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.finger1_enchant_id == None
    assert jack.finger1_enchant_quality == 0
    assert jack.finger1_enchant_name == 'None'
    assert jack.finger1_enchant_description == None

def test_audit_item_enchant_not_in_lookup():
    jack = Character('jack')
    response = { 'items' : {
        'finger1' : { 'tooltipParams' : { 'enchant' : 3000 }}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.finger1_enchant_id == 3000
    assert jack.finger1_enchant_quality == 0
    assert jack.finger1_enchant_name == 'None'
    assert jack.finger1_enchant_description == None

def test_audit_item_enchant_offhand_missing():
    jack = Character('jack')
    response = { 'items' : {},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.offHand_enchant_id == None
    assert jack.offHand_enchant_quality == None
    assert jack.offHand_enchant_name == None
    assert jack.offHand_enchant_description == None

def test_audit_item_enchant_offhand_not_enchantable():
    jack = Character('jack')
    response = { 'items' : {
        'offHand' : {}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.offHand_enchant_id == None
    assert jack.offHand_enchant_quality == None
    assert jack.offHand_enchant_name == None
    assert jack.offHand_enchant_description == None

def test_audit_item_hand_alliance():
    jack = Character('jack', faction_name='alliance')
    response = { 'items' : {
        'hand' : { 'tooltipParams' : { 'enchant' : 5932 }}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.hand_enchant_id == 5932
    assert jack.hand_enchant_quality == 4
    assert jack.hand_enchant_name == "Kul Tiran Herbalism"
    assert jack.hand_enchant_description == "Increase the speed of herb gathering on Kul Tiras and Zandalar"

def test_audit_item_hand_horde():
    jack = Character('jack', faction_name='horde')
    response = { 'items' : {
        'hand' : { 'tooltipParams' : { 'enchant' : 5932 }}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, None, None)

    assert jack.hand_enchant_id == 5932
    assert jack.hand_enchant_quality == 4
    assert jack.hand_enchant_name == "Zandalari Herbalism"
    assert jack.hand_enchant_description == "Increase the speed of herb gathering on Kul Tiras and Zandalar"

def test_audit_empty_sockets():
    jack = Character('jack')
    response = { 'items' : {},
        'audit' : { 'emptySockets' : 4 }}

    Section.audit(jack, response, None, None)

    assert jack.empty_sockets == 4

def test_audit_gem_in_db(db_session):
    jack = Character('jack')
    response = { 'items' : {
        'finger1' : { 'tooltipParams' : { 'gem0' : 153710 }}},
        'audit' : { 'emptySockets' : 0 }}

    Section.audit(jack, response, db_session, None)

    assert jack.gems[0].gem.id == 153710
    assert jack.gems[0].gem.quality == 2
    assert jack.gems[0].gem.name == 'Deadly Solstone'
    assert jack.gems[0].gem.icon == 'inv_jewelcrafting_80_cutgem01_orange'
    assert jack.gems[0].gem.stat == '+30 Critical Strike'
    assert jack.gems[0].slot == 'finger1'

def test_audit_gem_not_in_db(db_session, mock_api):
    jack = Character('jack')
    response = { 'items' : {
        'finger1' : { 'tooltipParams' : { 'gem0' : 12390 }}},
        'audit' : { 'emptySockets' : 0 }}

    mock_api.get_item.return_value = {
            'name' : 'Deadly Stone',
            'icon' : 'inv_fake',
            'gemInfo' : { 'bonus' : { 'name' : '+20 BS' }}}

    Section.audit(jack, response, db_session, mock_api)

    assert jack.gems[0].gem.id == 12390
    assert jack.gems[0].gem.quality == 1
    assert jack.gems[0].gem.name == 'Deadly Stone'
    assert jack.gems[0].gem.icon == 'inv_fake'
    assert jack.gems[0].gem.stat == '+20 BS'
    assert jack.gems[0].slot == 'finger1'

def test_audit_no_gems(db_session, mock_api):
    jack = Character('jack')
    response = { 'items' : {},
        'audit' : { 'emptySockets' : 4 }}

    Section.audit(jack, response, db_session, mock_api)

    assert jack.gems == []

