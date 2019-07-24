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

def test_profession_info_simple_primaries():
    data = { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}

    result = get_profession_info(data)

    primaries = [result[0], result[1]]

    assert ["Herbalism", 'trade_herbalism', '150+300|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] in primaries
    assert ["Mining", 'inv_pick_02', '122+300|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] in primaries

def test_profession_info_simple_secondaries():
    data = { 'primary' : [
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 },
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 }
            ]}

    result = get_profession_info(data)

    assert ["Cooking", 'inv_misc_food_15', '0+300|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] == result[2]
    assert ["Fishing", 'trade_fishing', '0+300|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] == result[3]
    assert ["Archaeology", 'trade_archaeology', '0+950'] == result[4]

def test_profession_info_primaries_all_expacs():
    data = { 'primary' : [
                {'id': 2486, 'name': 'Kul Tiran Enchanting', 'icon': 'trade_engraving', 'rank': 175, 'max': 150},
                {'id': 2487, 'name': 'Legion Enchanting', 'icon': 'trade_engraving', 'rank': 100, 'max': 100},
                {'id': 2488, 'name': 'Draenor Enchanting', 'icon': 'trade_engraving', 'rank': 100, 'max': 100},
                {'id': 2489, 'name': 'Pandaria Enchanting', 'icon': 'trade_engraving', 'rank': 75, 'max': 75},
                {'id': 2491, 'name': 'Cataclysm Enchanting', 'icon': 'trade_engraving', 'rank': 75, 'max': 75},
                {'id': 2492, 'name': 'Northrend Enchanting', 'icon': 'trade_engraving', 'rank': 75, 'max': 75},
                {'id': 2493, 'name': 'Outland Enchanting', 'icon': 'trade_engraving', 'rank': 75, 'max': 75},
                {'id': 197, 'name': 'Tailoring', 'icon': 'trade_tailoring', 'rank': 300, 'max': 300},
                {'id': 333, 'name': 'Enchanting', 'icon': 'trade_engraving', 'rank': 300, 'max': 300},
                {'id': 2533, 'name': 'Kul Tiran Tailoring', 'icon': 'trade_tailoring', 'rank': 175, 'max': 150},
                {'id': 2534, 'name': 'Legion Tailoring', 'icon': 'trade_tailoring', 'rank': 100, 'max': 100},
                {'id': 2535, 'name': 'Draenor Tailoring', 'icon': 'trade_tailoring', 'rank': 100, 'max': 100},
                {'id': 2536, 'name': 'Pandaria Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2537, 'name': 'Cataclysm Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2538, 'name': 'Northrend Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2539, 'name': 'Outland Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75}
            ],
            'secondary' : [
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 },
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 }
            ]}

    result = get_profession_info(data)

    primaries = [result[0], result[1]]

    assert ["Tailoring", 'trade_tailoring', '300+300|75+75|75+75|75+75|75+75|100+100|100+100|175+175'] in primaries
    assert ["Enchanting", 'trade_engraving', '300+300|75+75|75+75|75+75|75+75|100+100|100+100|175+175'] in primaries

def test_profession_info_secondaries_all_expacs():
    data = { 'primary' : [
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 },
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 }
            ],
            'secondary': [
                {'id': 2585, 'name': 'Kul Tiran Fishing', 'icon': 'trade_fishing', 'rank': 65, 'max': 150},
                {'id': 794, 'name': 'Archaeology', 'icon': 'trade_archaeology', 'rank': 600, 'max': 950},
                {'id': 2586, 'name': 'Legion Fishing', 'icon': 'trade_fishing', 'rank': 1, 'max': 100},
                {'id': 2587, 'name': 'Draenor Fishing', 'icon': 'trade_fishing', 'rank': 1, 'max': 100},
                {'id': 2588, 'name': 'Pandaria Fishing', 'icon': 'trade_fishing', 'rank': 75, 'max': 75},
                {'id': 2589, 'name': 'Cataclysm Fishing', 'icon': 'trade_fishing', 'rank': 75, 'max': 75},
                {'id': 2590, 'name': 'Northrend Fishing', 'icon': 'trade_fishing', 'rank': 75, 'max': 75},
                {'id': 2591, 'name': 'Outland Fishing', 'icon': 'trade_fishing', 'rank': 75, 'max': 75},
                {'id': 185, 'name': 'Cooking', 'icon': 'inv_misc_food_15', 'rank': 300, 'max': 300},
                {'id': 356, 'name': 'Fishing', 'icon': 'trade_fishing', 'rank': 300, 'max': 300},
                {'id': 2541, 'name': 'Kul Tiran Cooking', 'icon': 'inv_misc_food_15', 'rank': 175, 'max': 150},
                {'id': 2542, 'name': 'Legion Cooking', 'icon': 'inv_misc_food_15', 'rank': 1, 'max': 100},
                {'id': 2543, 'name': 'Draenor Cooking', 'icon': 'inv_misc_food_15', 'rank': 5, 'max': 100},
                {'id': 2544, 'name': 'Pandaria Cooking', 'icon': 'inv_misc_food_15', 'rank': 75, 'max': 75},
                {'id': 2545, 'name': 'Cataclysm Cooking', 'icon': 'inv_misc_food_15', 'rank': 75, 'max': 75},
                {'id': 2546, 'name': 'Northrend Cooking', 'icon': 'inv_misc_food_15', 'rank': 75, 'max': 75},
                {'id': 2547, 'name': 'Outland Cooking', 'icon': 'inv_misc_food_15', 'rank': 75, 'max': 75}
            ]}

    result = get_profession_info(data)

    assert ["Cooking", 'inv_misc_food_15', '300+300|75+75|75+75|75+75|75+75|5+100|1+100|175+175'] == result[2]
    assert ["Fishing", 'trade_fishing', '300+300|75+75|75+75|75+75|75+75|1+100|1+100|65+175'] == result[3]
    assert ["Archaeology", 'trade_archaeology', '600+950'] == result[4]

def test_profession_info_primaries_missing_expacs():
    data = { 'primary' : [
                {'id': 2486, 'name': 'Kul Tiran Enchanting', 'icon': 'trade_engraving', 'rank': 175, 'max': 150},
                {'id': 2487, 'name': 'Legion Enchanting', 'icon': 'trade_engraving', 'rank': 100, 'max': 100},
                {'id': 2488, 'name': 'Draenor Enchanting', 'icon': 'trade_engraving', 'rank': 100, 'max': 100},
                {'id': 197, 'name': 'Tailoring', 'icon': 'trade_tailoring', 'rank': 300, 'max': 300},
                {'id': 333, 'name': 'Enchanting', 'icon': 'trade_engraving', 'rank': 300, 'max': 300},
                {'id': 2533, 'name': 'Kul Tiran Tailoring', 'icon': 'trade_tailoring', 'rank': 175, 'max': 150},
                {'id': 2534, 'name': 'Legion Tailoring', 'icon': 'trade_tailoring', 'rank': 100, 'max': 100},
                {'id': 2535, 'name': 'Draenor Tailoring', 'icon': 'trade_tailoring', 'rank': 100, 'max': 100},
                {'id': 2536, 'name': 'Pandaria Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2537, 'name': 'Cataclysm Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2538, 'name': 'Northrend Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75},
                {'id': 2539, 'name': 'Outland Tailoring', 'icon': 'trade_tailoring', 'rank': 75, 'max': 75}
            ],
            'secondary' : [
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 },
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 }
            ]}

    result = get_profession_info(data)

    primaries = [result[0], result[1]]

    assert ["Tailoring", 'trade_tailoring', '300+300|75+75|75+75|75+75|75+75|100+100|100+100|175+175'] in primaries
    assert ["Enchanting", 'trade_engraving', '300+300|0+0|0+0|0+0|0+0|100+100|100+100|175+175'] in primaries

def test_professions_info_missing_primary():
    data  = { 'primary' : [
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 8, 'max' : 300 },
            ],
            'secondary' : [
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 },
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 }
            ]}


    result = get_profession_info(data)

    primaries = [result[0], result[1]]

    assert ["Mining", 'inv_pick_02', '8+300|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] in primaries
    assert ['', '', '0+0|0+0|0+0|0+0|0+0|0+0|0+0|0+0'] in primaries
