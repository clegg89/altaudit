#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for Professions
"""
import pytest

from charfetch import get_profession_info

def test_profession_info_name_simple_primaries():
    data = { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}

    result = get_profession_info(data, 0, 'us')

    primaries = [result[0], result[1]]

    assert ["Herbalism", 'trade_herbalism', '150+300'] in primaries
    assert ["Mining", 'inv_pick_02', '122+300'] in primaries

def test_profession_info_name_simple_secondaries():
    data = { 'primary' : [
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 },
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 }
            ]}

    result = get_profession_info(data, 0, 'us')

    assert ["Cooking", 'inv_misc_food_15', '0+300'] == result[2]
    assert ["Fishing", 'trade_fishing', '0+300'] == result[3]
    assert ["Archaeology", 'trade_archaeology', '0+950'] == result[4]
