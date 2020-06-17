"""Unit Tests for items info"""
import pytest

from unittest.mock import patch

from altaudit.models import Character, ITEM_SLOTS

import altaudit.sections.items as Section

@pytest.fixture
def mock_is_off_hand_weapon(mocker):
    return mocker.patch('altaudit.sections.items.is_off_hand_weapon')

@pytest.fixture
def make_fake_item():
    def _maker(slot, id_offset=0, ilvl=405):
        return {
                'slot' : { 'type' : slot.upper() },
                'level' : { 'value' : ilvl },
                'item' : { 'id' : 165822+id_offset },
                'name' : 'Cowl of Tideborne Omens',
                'quality' : { 'name' : 'Epic' } }

    return _maker

@pytest.fixture
def default_items_response(make_fake_item):
    items = []
    for i, k in enumerate(ITEM_SLOTS):
        items.append(make_fake_item(k, i))

    return { 'equipment' : { 'equipped_items' : items } }

def test_items_estimated_ilvl_default(default_items_response):
    jack = Character('jack')
    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 405

def test_items_estimated_ilvl_non_default(default_items_response):
    jack = Character('jack')
    for i,item in enumerate(default_items_response['equipment']['equipped_items']):
        item['level']['value'] = 405+i

    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 412.5

def test_items_estimated_ilvl_missing_is_zero(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]

    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 379.6875

def test_items_estimated_ilvl_missing_offhand_is_not_weapon(default_items_response, mock_is_off_hand_weapon):
    jack = Character('jack')
    default_items_response['equipment']['equipped_items'].remove(next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'OFF_HAND'))
    mock_is_off_hand_weapon.return_value = False

    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 405

def test_items_estimated_ilvl_missing_offhand_is_weapon(default_items_response, mock_is_off_hand_weapon):
    jack = Character('jack')
    default_items_response['equipment']['equipped_items'].remove(next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'OFF_HAND'))
    mock_is_off_hand_weapon.return_value = True

    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 379.6875

def test_items_all_items(default_items_response):
    jack = Character('jack')
    Section.items(jack, default_items_response, None, None)
    for i,slot in enumerate(ITEM_SLOTS):
        assert getattr(jack, '{}_itemLevel'.format(slot)) == 405
        assert getattr(jack, '{}_id'.format(slot)) == 165822+i
        assert getattr(jack, '{}_name'.format(slot)) == 'Cowl of Tideborne Omens'
        assert getattr(jack, '{}_quality'.format(slot)) == 'Epic'

def test_items_missing_item(default_items_response):
    jack = Character('jack')
    default_items_response['equipment']['equipped_items'].remove(next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'FINGER_1'))

    Section.items(jack, default_items_response, None, None)
    assert jack.finger_1_itemLevel == None
    assert jack.finger_1_id == None
    assert jack.finger_1_name == None
    assert jack.finger_1_quality == None

def test_items_missing_ilevel_is_None(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]['level']

    Section.items(jack, default_items_response, None, None)
    assert jack.head_itemLevel == None
    assert jack.head_id == 165822
    assert jack.head_name == 'Cowl of Tideborne Omens'
    assert jack.head_quality == 'Epic'
    assert jack.estimated_ilvl == 379.6875

def test_items_missing_ilevel_value_is_None(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]['level']['value']

    Section.items(jack, default_items_response, None, None)
    assert jack.head_itemLevel == None
    assert jack.head_id == 165822
    assert jack.head_name == 'Cowl of Tideborne Omens'
    assert jack.head_quality == 'Epic'
    assert jack.estimated_ilvl == 379.6875

def test_items_missing_id_value_is_None(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]['item']['id']

    Section.items(jack, default_items_response, None, None)
    assert jack.head_itemLevel == 405
    assert jack.head_id == None
    assert jack.head_name == 'Cowl of Tideborne Omens'
    assert jack.head_quality == 'Epic'

def test_items_missing_name_value_is_None(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]['name']

    Section.items(jack, default_items_response, None, None)
    assert jack.head_itemLevel == 405
    assert jack.head_id == 165822
    assert jack.head_name == None
    assert jack.head_quality == 'Epic'

def test_items_missing_quality_value_is_None(default_items_response):
    jack = Character('jack')
    del default_items_response['equipment']['equipped_items'][0]['quality']['name']

    Section.items(jack, default_items_response, None, None)
    assert jack.head_itemLevel == 405
    assert jack.head_id == 165822
    assert jack.head_name == 'Cowl of Tideborne Omens'
    assert jack.head_quality == None

def test_cloak_missing_name_desc(default_items_response):
    jack = Character('jack')
    cloak = next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'BACK')
    cloak['name'] = "Ashjra'kamas, Shroud of Resolve"

    Section.items(jack, default_items_response, None, None)
    assert jack.cloak_rank == None

def test_cloak_missing_display_string(default_items_response):
    jack = Character('jack')
    cloak = next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'BACK')
    cloak['name'] = "Ashjra'kamas, Shroud of Resolve"
    cloak['name_description'] = None

    Section.items(jack, default_items_response, None, None)
    assert jack.cloak_rank == None

def test_cloak_not_ashjrakamas(default_items_response):
    jack = Character('jack')

    Section.items(jack, default_items_response, None, None)
    assert jack.cloak_rank == None

def test_cloak_ashjrakamas_rank(default_items_response):
    jack = Character('jack')
    cloak = next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'BACK')
    cloak['name'] = "Ashjra'kamas, Shroud of Resolve"
    cloak['name_description'] = { 'display_string' : "Rank 12" }

    Section.items(jack, default_items_response, None, None)
    assert jack.cloak_rank == 12

def test_cloak_ashjrakamas_resistance(default_items_response):
    jack = Character('jack')
    cloak = next(item for item in default_items_response['equipment']['equipped_items'] if item['slot']['type'] == 'BACK')
    cloak['name'] = "Ashjra'kamas, Shroud of Resolve"
    cloak['name_description'] = { 'display_string' : "Rank 12" }
    cloak['stats'] = [{'type' : {'type' : 'CORRUPTION_RESISTANCE'}, 'value' : 86}]

    Section.items(jack, default_items_response, None, None)

def test_tabard_ignored(default_items_response):
    jack = Character('jack')
    default_items_response['equipment']['equipped_items'].append({
        'slot' : { 'type' : 'TABARD' },
        'level' : { 'value' : 1 },
        'item' : { 'id' : 45585 },
        'name' : 'Silvermoon City Tabard',
        'quality' : { 'name' : 'UNCOMMON' } })

    Section.items(jack, default_items_response, None, None)
    assert jack.estimated_ilvl == 405
