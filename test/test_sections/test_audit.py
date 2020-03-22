"""Unit Test for Audit Info"""
import pytest

from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, Gem
from altaudit.gem_enchant import gem_lookup

import altaudit.sections.audit as Section

@pytest.fixture
def mock_is_off_hand_weapon(mocker):
    return mocker.patch('altaudit.sections.audit.is_off_hand_weapon')

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

def test_audit_regular_item(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 6109,
                'source_item' : { 'name' : 'Enchant Ring - Accord of Haste' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 6109
    assert jack.finger_1_enchant_quality == 4
    assert jack.finger_1_enchant_name == 'Accord of Haste'
    assert jack.finger_1_enchant_description == '+60 Haste'

def test_audit_item_missing(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : []}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == None
    assert jack.finger_1_enchant_quality == 0
    assert jack.finger_1_enchant_name == 'None'
    assert jack.finger_1_enchant_description == None

def test_audit_item_no_enchant(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' }}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == None
    assert jack.finger_1_enchant_quality == 0
    assert jack.finger_1_enchant_name == 'None'
    assert jack.finger_1_enchant_description == None

def test_audit_item_enchant_not_in_lookup(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 3000,
                'source_item' : { 'name' : 'Enchant Ring - Total Garbage' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 3000
    assert jack.finger_1_enchant_quality == 1
    assert jack.finger_1_enchant_name == 'Total Garbage'
    assert jack.finger_1_enchant_description == None

def test_audit_item_enchant_offhand_missing_not_weapon(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : []}}
    mock_is_off_hand_weapon.return_value = False

    Section.audit(jack, response, None, None)

    assert jack.off_hand_enchant_id == None
    assert jack.off_hand_enchant_quality == None
    assert jack.off_hand_enchant_name == None
    assert jack.off_hand_enchant_description == None

def test_audit_item_enchant_offhand_not_enchantable(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'OFF_HAND' },
            'inventory_type' : { 'type' : 'HOLDABLE' }}]}}

    Section.audit(jack, response, None, None)

    assert jack.off_hand_enchant_id == None
    assert jack.off_hand_enchant_quality == None
    assert jack.off_hand_enchant_name == None
    assert jack.off_hand_enchant_description == None

def test_audit_item_enchant_weapon_offhand_is_enchanted(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'OFF_HAND' },
            'inventory_type' : { 'type' : 'WEAPON' },
            'enchantments' : [{
                'enchantment_id' : 5946,
                'source_item' : { 'name' : 'Enchant Weapon - Coastal Surge' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.off_hand_enchant_id == 5946
    assert jack.off_hand_enchant_quality == 4
    assert jack.off_hand_enchant_name == 'Coastal Surge'
    assert jack.off_hand_enchant_description == "Sometimes cause helpful spells to put a short heal over time effect on the target for 10 sec."

def test_audit_empty_sockets(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [
            { 'slot' : { 'type' : 'SHOULDER' }},
            { 'slot' : { 'type' : 'CHEST' }},
            { 'slot' : { 'type' : 'WAIST' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'WRIST' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'FINGER_1' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'FINGER_2' }, 'sockets' : [{}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.empty_sockets == 4
    assert jack.empty_socket_slots == 'waist|wrist|finger_1|finger_2'

def test_audit_enchant_dk_rune(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'MAIN_HAND' },
            'enchantments' : [{
                'enchantment_id' : 3368,
                'display_string' : 'Enchanted: Rune of the Fallen Crusader'}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.main_hand_enchant_id == 3368
    assert jack.main_hand_enchant_quality == 4
    assert jack.main_hand_enchant_name == 'Rune of the Fallen Crusader'
    assert jack.main_hand_enchant_description == "Chance to heal for 6% and increases total Strength by 15% for 15 sec."

def test_audit_gem_in_db(db_session, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Solstone',
                    'id' : 153710},
                'display_string' : '+30 Critical Strike'}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems[0].gem.id == 153710
    assert jack.gems[0].gem.quality == 2
    assert jack.gems[0].gem.name == 'Deadly Solstone'
    assert jack.gems[0].gem.icon == 'inv_jewelcrafting_80_cutgem01_orange'
    assert jack.gems[0].gem.stat == '+30 Critical Strike'
    assert jack.gems[0].slot == 'finger_1'

def test_audit_gem_missing_id(db_session, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Solstone'},
                'display_string' : '+30 Critical Strike'}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems == []

def test_audit_gem_missing_name_not_in_db(db_session, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'id' : 12390},
                'display_string' : '+20 Bullshit'}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems[0].gem.id == 12390
    assert jack.gems[0].gem.quality == 1
    assert jack.gems[0].gem.name == 'Unknown'
    assert jack.gems[0].gem.icon == None
    assert jack.gems[0].gem.stat == '+20 Bullshit'
    assert jack.gems[0].slot == 'finger_1'

def test_audit_gem_missing_display_string_not_in_db(db_session, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Stone',
                    'id' : 12390}}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems[0].gem.id == 12390
    assert jack.gems[0].gem.quality == 1
    assert jack.gems[0].gem.name == 'Deadly Stone'
    assert jack.gems[0].gem.icon == None
    assert jack.gems[0].gem.stat == "Unknown"
    assert jack.gems[0].slot == 'finger_1'

def test_audit_gem_not_in_db(db_session, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Stone',
                    'id' : 12390},
                'display_string' : '+20 Bullshit'}]}]}}

    Section.audit(jack, response, db_session, mock_api)

    assert jack.gems[0].gem.id == 12390
    assert jack.gems[0].gem.quality == 1
    assert jack.gems[0].gem.name == 'Deadly Stone'
    assert jack.gems[0].gem.icon == None
    assert jack.gems[0].gem.stat == '+20 Bullshit'
    assert jack.gems[0].slot == 'finger_1'

def test_audit_no_gems(db_session, mock_api, mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [
            { 'slot' : { 'type' : 'SHOULDER' }},
            { 'slot' : { 'type' : 'CHEST' }},
            { 'slot' : { 'type' : 'WAIST' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'WRIST' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'FINGER_1' }, 'sockets' : [{}]},
            { 'slot' : { 'type' : 'FINGER_2' }, 'sockets' : [{}]}]}}

    Section.audit(jack, response, db_session, mock_api)

    assert jack.gems == []

def test_audit_missing_enchant_id(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'source_item' : { 'name' : 'Enchant Ring - Accord of Haste' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == None
    assert jack.finger_1_enchant_quality == 1
    assert jack.finger_1_enchant_name == "Accord of Haste"
    assert jack.finger_1_enchant_description == None

def test_audit_missing_enchant_source_item_and_display_string_in_lookup(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 6109}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 6109
    assert jack.finger_1_enchant_quality == 4
    assert jack.finger_1_enchant_name == "Accord of Haste"
    assert jack.finger_1_enchant_description == '+60 Haste'

def test_audit_missing_enchant_source_item_and_display_string_not_in_lookup(mock_is_off_hand_weapon):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 3000}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 3000
    assert jack.finger_1_enchant_quality == 1
    assert jack.finger_1_enchant_name == "Unknown"
    assert jack.finger_1_enchant_description == None
