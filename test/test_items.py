#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Unit Tests for Item related code
"""
import pytest

from charfetch import get_all_items
from charfetch.character import _get_item

@pytest.fixture
def fake_hoa():
    return {'id': 158075, 'name': 'Heart of Azeroth', 'icon': 'inv_heartofazeroth', 'quality': 6, 'itemLevel': 427, 'azeriteItem': {'azeriteLevel': 47, 'azeriteExperience': 1062, 'azeriteExperienceRemaining': 22815}}

@pytest.fixture
def fake_neck():
    return {'id': 122666, 'name': 'Eternal Woven Ivy Necklace', 'icon': 'inv_misc_herb_15', 'quality': 7, 'itemLevel': 65}

@pytest.fixture
def make_fake_item():
    def _make_fake_item(offset=0):
        return {'id': 165822+offset, 'name': 'Cowl of Tideborne Omens', 'icon': 'inv_helm_cloth_zuldazarraid_d_01', 'quality': 4, 'itemLevel': 405}

    return _make_fake_item

@pytest.fixture
def item_slots():
    return ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']

@pytest.fixture
def default_item_dictionary(item_slots, make_fake_item, fake_hoa):
    items_dict = {}

    for i, k in enumerate(item_slots):
        items_dict[k] = make_fake_item(i)

    items_dict['neck'] = fake_hoa

    return items_dict

def test_get_item(make_fake_item):
    assert _get_item(make_fake_item()) == [405, 165822, 'Cowl of Tideborne Omens', 'inv_helm_cloth_zuldazarraid_d_01', 4]

def test_get_item_none():
    assert _get_item(None) == [None, None, None, None, None]

def test_get_all_items_equipped_ilevel_default(default_item_dictionary):
    assert get_all_items(default_item_dictionary)[0] == 406.375

def test_get_all_items_equipped_ilevel_default(default_item_dictionary):
    for i,k in enumerate(default_item_dictionary.keys()):
        default_item_dictionary[k]['itemLevel'] = 405+i

    assert get_all_items(default_item_dictionary)[0] == 412.5

def test_get_all_items_equipped_ilevel_missing_is_zero(default_item_dictionary):
    del default_item_dictionary['head']

    assert get_all_items(default_item_dictionary)[0] == 381.0625

def test_get_all_items_equipped_ilevel_missing_offhand_assumed_2h(default_item_dictionary):
    del default_item_dictionary['offHand']
    default_item_dictionary['mainHand']['itemLevel'] = 425

    assert get_all_items(default_item_dictionary)[0] == 408.875

def test_get_all_items_items_in_order(default_item_dictionary, item_slots):
    result = get_all_items(default_item_dictionary)

    assert result[1] == _get_item(default_item_dictionary[item_slots[0]])
    assert result[2] == _get_item(default_item_dictionary[item_slots[1]])
    assert result[3] == _get_item(default_item_dictionary[item_slots[2]])
    assert result[4] == _get_item(default_item_dictionary[item_slots[3]])
    assert result[5] == _get_item(default_item_dictionary[item_slots[4]])
    assert result[6] == _get_item(default_item_dictionary[item_slots[5]])
    assert result[7] == _get_item(default_item_dictionary[item_slots[6]])
    assert result[8] == _get_item(default_item_dictionary[item_slots[7]])
    assert result[9] == _get_item(default_item_dictionary[item_slots[8]])
    assert result[10] == _get_item(default_item_dictionary[item_slots[9]])
    assert result[11] == _get_item(default_item_dictionary[item_slots[10]])
    assert result[12] == _get_item(default_item_dictionary[item_slots[11]])
    assert result[13] == _get_item(default_item_dictionary[item_slots[12]])
    assert result[14] == _get_item(default_item_dictionary[item_slots[13]])
    assert result[15] == _get_item(default_item_dictionary[item_slots[14]])
    assert result[16] == _get_item(default_item_dictionary[item_slots[15]])

def test_get_all_items_ilevels_missing_is_None_item(default_item_dictionary, item_slots):
    del default_item_dictionary['finger1']
    result = get_all_items(default_item_dictionary)

    assert result[item_slots.index('finger1')+1] == _get_item(None)
