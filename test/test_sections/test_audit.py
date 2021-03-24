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

@pytest.fixture
def mock_is_primary_slot(mocker):
    mock = mocker.patch('altaudit.sections.audit.is_primary_enchant_slot')
    mock.return_value = False
    return mock

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

def test_audit_regular_item(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 6166,
                'source_item' : { 'name' : 'Enchant Ring - Tenet of Haste' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 6166
    assert jack.finger_1_enchant_quality == 3
    assert jack.finger_1_enchant_name == 'Tenet of Haste'
    assert jack.finger_1_enchant_description == '+16 Haste'

def test_audit_item_missing(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : []}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == None
    assert jack.finger_1_enchant_quality == 0
    assert jack.finger_1_enchant_name == 'None'
    assert jack.finger_1_enchant_description == None

def test_audit_item_no_enchant(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' }}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == None
    assert jack.finger_1_enchant_quality == 0
    assert jack.finger_1_enchant_name == 'None'
    assert jack.finger_1_enchant_description == None

def test_audit_item_enchant_not_in_lookup(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_item_enchant_offhand_missing_not_weapon(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : []}}
    mock_is_off_hand_weapon.return_value = False

    Section.audit(jack, response, None, None)

    assert jack.off_hand_enchant_id == None
    assert jack.off_hand_enchant_quality == None
    assert jack.off_hand_enchant_name == None
    assert jack.off_hand_enchant_description == None

def test_audit_item_enchant_offhand_not_enchantable(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_item_enchant_weapon_offhand_is_enchanted(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'OFF_HAND' },
            'inventory_type' : { 'type' : 'WEAPON' },
            'enchantments' : [{
                'enchantment_id' : 6223,
                'source_item' : { 'name' : 'Enchant Weapon - Lightless Force' }}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.off_hand_enchant_id == 6223
    assert jack.off_hand_enchant_quality == 3
    assert jack.off_hand_enchant_name == 'Lightless Force'
    assert jack.off_hand_enchant_description == "Chance to send out a wave of Shadow energy, striking 5 enemies"

def test_audit_empty_sockets(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_enchant_dk_rune(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_gem_in_db(db_session, mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Jewel Doublet',
                    'id' : 173121},
                'display_string' : '+12 Critical Strike'}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems[0].gem.id == 173121
    assert jack.gems[0].gem.quality == 2
    assert jack.gems[0].gem.name == 'Deadly Jewel Doublet'
    assert jack.gems[0].gem.icon == 'inv_jewelcrafting_90_cutuncommon_orange'
    assert jack.gems[0].gem.stat == '+12 Critical Strike'
    assert jack.gems[0].slot == 'finger_1'

def test_audit_gem_missing_id(db_session, mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'sockets' : [{
                'item' : {
                    'name' : 'Deadly Jewel Doublet'},
                'display_string' : '+12 Critical Strike'}]}]}}

    Section.audit(jack, response, db_session, None)

    assert jack.gems == []

def test_audit_gem_missing_name_not_in_db(db_session, mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_gem_missing_display_string_not_in_db(db_session, mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_gem_not_in_db(db_session, mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_no_gems(db_session, mock_api, mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_missing_enchant_id(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_missing_enchant_source_item_and_display_string_in_lookup(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'FINGER_1' },
            'enchantments' : [{
                'enchantment_id' : 6166}]}]}}

    Section.audit(jack, response, None, None)

    assert jack.finger_1_enchant_id == 6166
    assert jack.finger_1_enchant_quality == 3
    assert jack.finger_1_enchant_name == "Tenet of Haste"
    assert jack.finger_1_enchant_description == '+16 Haste'

def test_audit_missing_enchant_source_item_and_display_string_not_in_lookup(mock_is_off_hand_weapon, mock_is_primary_slot):
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

def test_audit_primary_wrists(mock_is_off_hand_weapon, mock_is_primary_slot):
    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'WRIST' },
            'enchantments' : [{
                'enchantment_id' : 6220,
                'source_item' : { 'name' : 'Enchant Bracers - Eternal Intellect' }}]}]}}
    mock_is_primary_slot.return_value = True

    Section.audit(jack, response, None, None)

    assert jack.primary_enchant_id == 6220
    assert jack.primary_enchant_quality == 3
    assert jack.primary_enchant_name == "Eternal Intellect"
    assert jack.primary_enchant_description == '+15 Intellect'

def test_audit_primary_wrists_but_wearing_unrelated(mock_is_off_hand_weapon, mock_is_primary_slot):
    def _is_primary_slot(profile, slot):
        if slot == 'wrist':
            return True
        else:
            return False

    jack = Character('jack')
    response = { 'equipment' : {
        'equipped_items' : [{
            'slot' : { 'type' : 'WRIST' },
            'enchantments' : [{
                'enchantment_id' : 6220,
                'source_item' : { 'name' : 'Enchant Bracers - Eternal Intellect' }}]},
        {
            'slot' : { 'type' : "FEET" },
            'enchantments' : [{
                'enchantment_id' : 6221,
                'source_item' : { 'name' : 'Enchant Boots - Eternal Agility'}}]}]}}
    mock_is_primary_slot.side_effect = _is_primary_slot

    Section.audit(jack, response, None, None)

    assert jack.primary_enchant_id == 6220
    assert jack.primary_enchant_quality == 3
    assert jack.primary_enchant_name == "Eternal Intellect"
    assert jack.primary_enchant_description == '+15 Intellect'
