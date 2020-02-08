"""Unit Tests for items info"""
import pytest

from altaudit.models import Character, ITEM_SLOTS

import altaudit.sections as Section

@pytest.fixture
def make_fake_item():
    def _maker(id_offset=0, ilvl=405):
        return {'id': 165822+id_offset, 'name': 'Cowl of Tideborne Omens', 'icon': 'inv_helm_cloth_zuldazarraid_d_01', 'quality': 4, 'itemLevel': ilvl}

    return _maker

@pytest.fixture
def default_items_response(make_fake_item):
    items = {}
    for i, k in enumerate(ITEM_SLOTS):
        items[k] = make_fake_item(i)

    return { 'items' : items }

def test_items_estimated_ilvl_default(default_items_response):
    jack = Character('jack')
    Section.items(jack, default_items_response)
    assert jack.estimated_ilvl == 405

def test_items_estimated_ilvl_non_default(default_items_response):
    jack = Character('jack')
    for i,k in enumerate(default_items_response['items'].keys()):
        default_items_response['items'][k]['itemLevel'] = 405+i

    Section.items(jack, default_items_response)
    assert jack.estimated_ilvl == 412.5

def test_items_estimated_ilvl_missing_is_zero(default_items_response):
    jack = Character('jack')
    del default_items_response['items']['head']

    Section.items(jack, default_items_response)
    assert jack.estimated_ilvl == 379.6875

def test_items_estimated_ilvl_missing_offhand_assumed_2h(default_items_response):
    jack = Character('jack')
    del default_items_response['items']['offHand']

    Section.items(jack, default_items_response)
    assert jack.estimated_ilvl == 405

def test_items_all_items(default_items_response):
    jack = Character('jack')
    Section.items(jack, default_items_response)
    for i,slot in enumerate(ITEM_SLOTS):
        assert getattr(jack, '{}_itemLevel'.format(slot)) == 405
        assert getattr(jack, '{}_id'.format(slot)) == 165822+i
        assert getattr(jack, '{}_name'.format(slot)) == 'Cowl of Tideborne Omens'
        assert getattr(jack, '{}_icon'.format(slot)) == 'inv_helm_cloth_zuldazarraid_d_01'
        assert getattr(jack, '{}_quality'.format(slot)) == 4

def test_items_missing_item(default_items_response):
    jack = Character('jack')
    del default_items_response['items']['offHand']
    Section.items(jack, default_items_response)
    assert jack.offHand_itemLevel == None
    assert jack.offHand_id == None
    assert jack.offHand_name == None
    assert jack.offHand_icon == None
    assert jack.offHand_quality == None
