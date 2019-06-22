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

from charfetch import get_all_items, Item, ItemManager
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
def default_item_dictionary(make_fake_item, fake_hoa):
    items_dict = {}
    items = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']

    for i, k in enumerate(items):
        items_dict[k] = make_fake_item(i)

    items_dict['neck'] = fake_hoa

    return items_dict

def test_get_item(make_fake_item):
    assert _get_item(make_fake_item()) == [405, 165822, 'Cowl of Tideborne Omens', 'inv_helm_cloth_zuldazarraid_d_01', 4]

def test_get_all_items_quipped_ilevel_default(default_item_dictionary):
    assert get_all_items(default_item_dictionary)[0] == 406.375

def test_get_all_items_quipped_ilevel_default(default_item_dictionary):
    for i,k in enumerate(default_item_dictionary.keys()):
        default_item_dictionary[k]['itemLevel'] = 405+i

    assert get_all_items(default_item_dictionary)[0] == 412.5

class TestItem:
    def test_item_serialize(self, make_fake_item):
        assert Item(make_fake_item()).serialize() == [405, 165822, 'Cowl of Tideborne Omens', 'inv_helm_cloth_zuldazarraid_d_01', 4]

    def test_item_equals(self, make_fake_item):
        fake = make_fake_item()
        other_fake = make_fake_item(1)
        other_fake['name'] += ' 2'
        other_fake['icon'] += '_2'
        other_fake['quality'] += 3
        other_fake['itemLevel'] += 10
        assert Item(fake) == Item(fake)
        assert Item(fake) != Item(other_fake)
        assert Item(fake) != 5 # check that it won't try to compare itself to other objects

class TestItemManager:
    def test_azerite_info_no_neck(self):
        im = ItemManager({})
        assert not im.hoa_level
        assert not im.hoa_exp
        assert not im.hoa_exp_rem

    def test_azerite_info_neck_not_hoa(self, fake_neck):
        im = ItemManager({ 'neck' : fake_neck })
        assert not im.hoa_level
        assert not im.hoa_exp
        assert not im.hoa_exp_rem

    def test_azerite_info_hoa(self, fake_hoa):
        im = ItemManager({ 'neck' : fake_hoa })
        assert im.hoa_level == fake_hoa['azeriteItem']['azeriteLevel']
        assert im.hoa_exp == fake_hoa['azeriteItem']['azeriteExperience']
        assert im.hoa_exp_rem == fake_hoa['azeriteItem']['azeriteExperienceRemaining']

    def test_item_info(self, default_item_dictionary):
        im = ItemManager(default_item_dictionary)
        for k,v in default_item_dictionary.items():
            assert im.items[k] == Item(v)

    def test_equipped_ilvl(self, default_item_dictionary):
        im = ItemManager(default_item_dictionary)
        expected = 0
        for v in default_item_dictionary.values():
            expected += v['itemLevel']

        expected /= len(default_item_dictionary.keys())

        assert im.equipped_ilvl == expected

    def test_serialize(self, default_item_dictionary):
        im = ItemManager(default_item_dictionary)
        result = im.serialize()

        assert result[0] == im.equipped_ilvl
        assert result[1] == im.hoa_level
        assert result[2] == im.hoa_exp
        assert result[3] == im.hoa_exp_rem
        assert result[4] == im.items['head'].serialize()
        assert result[5] == im.items['neck'].serialize()
        assert result[6] == im.items['shoulder'].serialize()
        assert result[7] == im.items['back'].serialize()
        assert result[8] == im.items['chest'].serialize()
        assert result[9] == im.items['wrist'].serialize()
        assert result[10] == im.items['hands'].serialize()
        assert result[11] == im.items['waist'].serialize()
        assert result[12] == im.items['legs'].serialize()
        assert result[13] == im.items['feet'].serialize()
        assert result[14] == im.items['finger1'].serialize()
        assert result[15] == im.items['finger2'].serialize()
        assert result[16] == im.items['trinket1'].serialize()
        assert result[17] == im.items['trinket2'].serialize()
        assert result[18] == im.items['mainHand'].serialize()
        assert result[19] == im.items['offHand'].serialize()

    def test_serialize_missing_items(self, default_item_dictionary):
        del default_item_dictionary['offHand']
        del default_item_dictionary['finger1']

        im = ItemManager(default_item_dictionary)
        result = im.serialize()

        assert result[0] == im.equipped_ilvl
        assert result[1] == im.hoa_level
        assert result[2] == im.hoa_exp
        assert result[3] == im.hoa_exp_rem
        assert result[4] == im.items['head'].serialize()
        assert result[5] == im.items['neck'].serialize()
        assert result[6] == im.items['shoulder'].serialize()
        assert result[7] == im.items['back'].serialize()
        assert result[8] == im.items['chest'].serialize()
        assert result[9] == im.items['wrist'].serialize()
        assert result[10] == im.items['hands'].serialize()
        assert result[11] == im.items['waist'].serialize()
        assert result[12] == im.items['legs'].serialize()
        assert result[13] == im.items['feet'].serialize()
        assert result[14] == None
        assert result[15] == im.items['finger2'].serialize()
        assert result[16] == im.items['trinket1'].serialize()
        assert result[17] == im.items['trinket2'].serialize()
        assert result[18] == im.items['mainHand'].serialize()
        assert result[19] == None
