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

from charfetch import Item, ItemManager

@pytest.fixture
def fake_hoa():
    return {'id': 158075, 'name': 'Heart of Azeroth', 'icon': 'inv_heartofazeroth', 'quality': 6, 'itemLevel': 427, 'azeriteItem': {'azeriteLevel': 47, 'azeriteExperience': 1062, 'azeriteExperienceRemaining': 22815}}

@pytest.fixture
def fake_neck():
    return {'id': 122666, 'name': 'Eternal Woven Ivy Necklace', 'icon': 'inv_misc_herb_15', 'quality': 7, 'itemLevel': 65}

@pytest.fixture
def fake_item():
    return

@pytest.fixture
def make_fake_item():
    def _make_fake_item(offset=0):
        return {'id': 165822+offset, 'name': 'Cowl of Tideborne Omens', 'icon': 'inv_helm_cloth_zuldazarraid_d_01', 'quality': 4, 'itemLevel': 405}

    return _make_fake_item

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
        assert im.hoa_level == ''
        assert im.hoa_exp == ''
        assert im.hoa_exp_rem == ''

    def test_azerite_info_neck_not_hoa(self, fake_neck):
        im = ItemManager({ 'neck' : fake_neck })
        assert im.hoa_level == ''
        assert im.hoa_exp == ''
        assert im.hoa_exp_rem == ''

    def test_azerite_info_hoa(self, fake_hoa):
        im = ItemManager({ 'neck' : fake_hoa })
        assert im.hoa_level == fake_hoa['azeriteItem']['azeriteLevel']
        assert im.hoa_exp == fake_hoa['azeriteItem']['azeriteExperience']
        assert im.hoa_exp_rem == fake_hoa['azeriteItem']['azeriteExperienceRemaining']

    def test_item_info(self, make_fake_item, fake_hoa):
        items_dict = {}
        items = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']

        for i, k in enumerate(items):
            items_dict[k] = make_fake_item(i)

        items_dict['neck'] = fake_hoa

        im = ItemManager(items_dict)
        for k,v in items_dict.items():
            assert im.items[k] == Item(v)
