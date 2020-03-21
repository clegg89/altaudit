"""Unit Tests for Profesion Info"""
import pytest

from altaudit.models import Character

import altaudit.sections.professions as Section

def test_profession_simple_priamries():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}}

    Section.professions(jack, response)

    assert jack.primary1_name == 'Herbalism'
    assert jack.primary1_icon == 'trade_herbalism'
    assert jack.primary1_classic_level == 150
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == None
    assert jack.primary1_burning_crusade_max == None
    assert jack.primary1_wrath_of_the_lich_king_level == None
    assert jack.primary1_wrath_of_the_lich_king_max == None
    assert jack.primary1_cataclysm_level == None
    assert jack.primary1_cataclysm_max == None
    assert jack.primary1_mists_of_pandaria_level == None
    assert jack.primary1_mists_of_pandaria_max == None
    assert jack.primary1_warlords_of_draenor_level == None
    assert jack.primary1_warlords_of_draenor_max == None
    assert jack.primary1_legion_level == None
    assert jack.primary1_legion_max == None
    assert jack.primary1_battle_for_azeroth_level == None
    assert jack.primary1_battle_for_azeroth_max == None
    assert jack.primary2_name == 'Mining'
    assert jack.primary2_icon == 'inv_pick_02'
    assert jack.primary2_classic_level == 122
    assert jack.primary2_classic_max == 300
    assert jack.primary2_burning_crusade_level == None
    assert jack.primary2_burning_crusade_max == None
    assert jack.primary2_wrath_of_the_lich_king_level == None
    assert jack.primary2_wrath_of_the_lich_king_max == None
    assert jack.primary2_cataclysm_level == None
    assert jack.primary2_cataclysm_max == None
    assert jack.primary2_mists_of_pandaria_level == None
    assert jack.primary2_mists_of_pandaria_max == None
    assert jack.primary2_warlords_of_draenor_level == None
    assert jack.primary2_warlords_of_draenor_max == None
    assert jack.primary2_legion_level == None
    assert jack.primary2_legion_max == None
    assert jack.primary2_battle_for_azeroth_level == None
    assert jack.primary2_battle_for_azeroth_max == None

def test_profession_simple_secondaries():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}}

    Section.professions(jack, response)

    assert jack.cooking_name == 'Cooking'
    assert jack.cooking_icon == 'inv_misc_food_15'
    assert jack.cooking_classic_level == 0
    assert jack.cooking_classic_max == 300
    assert jack.cooking_burning_crusade_level == None
    assert jack.cooking_burning_crusade_max == None
    assert jack.cooking_wrath_of_the_lich_king_level == None
    assert jack.cooking_wrath_of_the_lich_king_max == None
    assert jack.cooking_cataclysm_level == None
    assert jack.cooking_cataclysm_max == None
    assert jack.cooking_mists_of_pandaria_level == None
    assert jack.cooking_mists_of_pandaria_max == None
    assert jack.cooking_warlords_of_draenor_level == None
    assert jack.cooking_warlords_of_draenor_max == None
    assert jack.cooking_legion_level == None
    assert jack.cooking_legion_max == None
    assert jack.cooking_battle_for_azeroth_level == None
    assert jack.cooking_battle_for_azeroth_max == None
    assert jack.fishing_name == 'Fishing'
    assert jack.fishing_icon == 'trade_fishing'
    assert jack.fishing_classic_level == 0
    assert jack.fishing_classic_max == 300
    assert jack.fishing_burning_crusade_level == None
    assert jack.fishing_burning_crusade_max == None
    assert jack.fishing_wrath_of_the_lich_king_level == None
    assert jack.fishing_wrath_of_the_lich_king_max == None
    assert jack.fishing_cataclysm_level == None
    assert jack.fishing_cataclysm_max == None
    assert jack.fishing_mists_of_pandaria_level == None
    assert jack.fishing_mists_of_pandaria_max == None
    assert jack.fishing_warlords_of_draenor_level == None
    assert jack.fishing_warlords_of_draenor_max == None
    assert jack.fishing_legion_level == None
    assert jack.fishing_legion_max == None
    assert jack.fishing_battle_for_azeroth_level == None
    assert jack.fishing_battle_for_azeroth_max == None
    assert jack.archaeology_name == 'Archaeology'
    assert jack.archaeology_icon == 'trade_archaeology'
    assert jack.archaeology_level == 0
    assert jack.archaeology_max == 950

def test_profession_primaries_all_expacs():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
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
            ]}}

    Section.professions(jack, response)

    assert jack.primary1_name == 'Enchanting'
    assert jack.primary1_icon == 'trade_engraving'
    assert jack.primary1_classic_level == 300
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == 75
    assert jack.primary1_burning_crusade_max == 75
    assert jack.primary1_wrath_of_the_lich_king_level == 75
    assert jack.primary1_wrath_of_the_lich_king_max == 75
    assert jack.primary1_cataclysm_level == 75
    assert jack.primary1_cataclysm_max == 75
    assert jack.primary1_mists_of_pandaria_level == 75
    assert jack.primary1_mists_of_pandaria_max == 75
    assert jack.primary1_warlords_of_draenor_level == 100
    assert jack.primary1_warlords_of_draenor_max == 100
    assert jack.primary1_legion_level == 100
    assert jack.primary1_legion_max == 100
    assert jack.primary1_battle_for_azeroth_level == 175
    assert jack.primary1_battle_for_azeroth_max == 175
    assert jack.primary2_name == 'Tailoring'
    assert jack.primary2_icon == 'trade_tailoring'
    assert jack.primary2_classic_level == 300
    assert jack.primary2_classic_max == 300
    assert jack.primary2_burning_crusade_level == 75
    assert jack.primary2_burning_crusade_max == 75
    assert jack.primary2_wrath_of_the_lich_king_level == 75
    assert jack.primary2_wrath_of_the_lich_king_max == 75
    assert jack.primary2_cataclysm_level == 75
    assert jack.primary2_cataclysm_max == 75
    assert jack.primary2_mists_of_pandaria_level == 75
    assert jack.primary2_mists_of_pandaria_max == 75
    assert jack.primary2_warlords_of_draenor_level == 100
    assert jack.primary2_warlords_of_draenor_max == 100
    assert jack.primary2_legion_level == 100
    assert jack.primary2_legion_max == 100
    assert jack.primary2_battle_for_azeroth_level == 175
    assert jack.primary2_battle_for_azeroth_max == 175

def test_profession_secondaries_all_expacs():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
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
            ]}}

    Section.professions(jack, response)

    assert jack.cooking_name == 'Cooking'
    assert jack.cooking_icon == 'inv_misc_food_15'
    assert jack.cooking_classic_level == 300
    assert jack.cooking_classic_max == 300
    assert jack.cooking_burning_crusade_level == 75
    assert jack.cooking_burning_crusade_max == 75
    assert jack.cooking_wrath_of_the_lich_king_level == 75
    assert jack.cooking_wrath_of_the_lich_king_max == 75
    assert jack.cooking_cataclysm_level == 75
    assert jack.cooking_cataclysm_max == 75
    assert jack.cooking_mists_of_pandaria_level == 75
    assert jack.cooking_mists_of_pandaria_max == 75
    assert jack.cooking_warlords_of_draenor_level == 5
    assert jack.cooking_warlords_of_draenor_max == 100
    assert jack.cooking_legion_level == 1
    assert jack.cooking_legion_max == 100
    assert jack.cooking_battle_for_azeroth_level == 175
    assert jack.cooking_battle_for_azeroth_max == 175
    assert jack.fishing_name == 'Fishing'
    assert jack.fishing_icon == 'trade_fishing'
    assert jack.fishing_classic_level == 300
    assert jack.fishing_classic_max == 300
    assert jack.fishing_burning_crusade_level == 75
    assert jack.fishing_burning_crusade_max == 75
    assert jack.fishing_wrath_of_the_lich_king_level == 75
    assert jack.fishing_wrath_of_the_lich_king_max == 75
    assert jack.fishing_cataclysm_level == 75
    assert jack.fishing_cataclysm_max == 75
    assert jack.fishing_mists_of_pandaria_level == 75
    assert jack.fishing_mists_of_pandaria_max == 75
    assert jack.fishing_warlords_of_draenor_level == 1
    assert jack.fishing_warlords_of_draenor_max == 100
    assert jack.fishing_legion_level == 1
    assert jack.fishing_legion_max == 100
    assert jack.fishing_battle_for_azeroth_level == 65
    assert jack.fishing_battle_for_azeroth_max == 175
    assert jack.archaeology_name == 'Archaeology'
    assert jack.archaeology_icon == 'trade_archaeology'
    assert jack.archaeology_level == 600
    assert jack.archaeology_max == 950

def test_profession_primaries_missing_expacs():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
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
            ]}}

    Section.professions(jack, response)

    assert jack.primary1_name == 'Enchanting'
    assert jack.primary1_icon == 'trade_engraving'
    assert jack.primary1_classic_level == 300
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == None
    assert jack.primary1_burning_crusade_max == None
    assert jack.primary1_wrath_of_the_lich_king_level == None
    assert jack.primary1_wrath_of_the_lich_king_max == None
    assert jack.primary1_cataclysm_level == None
    assert jack.primary1_cataclysm_max == None
    assert jack.primary1_mists_of_pandaria_level == None
    assert jack.primary1_mists_of_pandaria_max == None
    assert jack.primary1_warlords_of_draenor_level == 100
    assert jack.primary1_warlords_of_draenor_max == 100
    assert jack.primary1_legion_level == 100
    assert jack.primary1_legion_max == 100
    assert jack.primary1_battle_for_azeroth_level == 175
    assert jack.primary1_battle_for_azeroth_max == 175
    assert jack.primary2_name == 'Tailoring'
    assert jack.primary2_icon == 'trade_tailoring'
    assert jack.primary2_classic_level == 300
    assert jack.primary2_classic_max == 300
    assert jack.primary2_burning_crusade_level == 75
    assert jack.primary2_burning_crusade_max == 75
    assert jack.primary2_wrath_of_the_lich_king_level == 75
    assert jack.primary2_wrath_of_the_lich_king_max == 75
    assert jack.primary2_cataclysm_level == 75
    assert jack.primary2_cataclysm_max == 75
    assert jack.primary2_mists_of_pandaria_level == 75
    assert jack.primary2_mists_of_pandaria_max == 75
    assert jack.primary2_warlords_of_draenor_level == 100
    assert jack.primary2_warlords_of_draenor_max == 100
    assert jack.primary2_legion_level == 100
    assert jack.primary2_legion_max == 100
    assert jack.primary2_battle_for_azeroth_level == 175
    assert jack.primary2_battle_for_azeroth_max == 175

def test_professions_missing_primary():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}}

    Section.professions(jack, response)

    assert jack.primary1_name == 'Herbalism'
    assert jack.primary1_icon == 'trade_herbalism'
    assert jack.primary1_classic_level == 150
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == None
    assert jack.primary1_burning_crusade_max == None
    assert jack.primary1_wrath_of_the_lich_king_level == None
    assert jack.primary1_wrath_of_the_lich_king_max == None
    assert jack.primary1_cataclysm_level == None
    assert jack.primary1_cataclysm_max == None
    assert jack.primary1_mists_of_pandaria_level == None
    assert jack.primary1_mists_of_pandaria_max == None
    assert jack.primary1_warlords_of_draenor_level == None
    assert jack.primary1_warlords_of_draenor_max == None
    assert jack.primary1_legion_level == None
    assert jack.primary1_legion_max == None
    assert jack.primary1_battle_for_azeroth_level == None
    assert jack.primary1_battle_for_azeroth_max == None
    assert jack.primary2_name == None
    assert jack.primary2_icon == None
    assert jack.primary2_classic_level == None
    assert jack.primary2_classic_max == None
    assert jack.primary2_burning_crusade_level == None
    assert jack.primary2_burning_crusade_max == None
    assert jack.primary2_wrath_of_the_lich_king_level == None
    assert jack.primary2_wrath_of_the_lich_king_max == None
    assert jack.primary2_cataclysm_level == None
    assert jack.primary2_cataclysm_max == None
    assert jack.primary2_mists_of_pandaria_level == None
    assert jack.primary2_mists_of_pandaria_max == None
    assert jack.primary2_warlords_of_draenor_level == None
    assert jack.primary2_warlords_of_draenor_max == None
    assert jack.primary2_legion_level == None
    assert jack.primary2_legion_max == None
    assert jack.primary2_battle_for_azeroth_level == None
    assert jack.primary2_battle_for_azeroth_max == None

def test_professions_missing_icon():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 202, 'name' : "Engineering", 'rank' : 1, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}}

    Section.professions(jack, response)

    assert jack.primary1_name == 'Herbalism'
    assert jack.primary1_icon == 'trade_herbalism'
    assert jack.primary1_classic_level == 150
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == None
    assert jack.primary1_burning_crusade_max == None
    assert jack.primary1_wrath_of_the_lich_king_level == None
    assert jack.primary1_wrath_of_the_lich_king_max == None
    assert jack.primary1_cataclysm_level == None
    assert jack.primary1_cataclysm_max == None
    assert jack.primary1_mists_of_pandaria_level == None
    assert jack.primary1_mists_of_pandaria_max == None
    assert jack.primary1_warlords_of_draenor_level == None
    assert jack.primary1_warlords_of_draenor_max == None
    assert jack.primary1_legion_level == None
    assert jack.primary1_legion_max == None
    assert jack.primary1_battle_for_azeroth_level == None
    assert jack.primary1_battle_for_azeroth_max == None
    assert jack.primary2_name == 'Engineering'
    assert jack.primary2_icon == None
    assert jack.primary2_classic_level == 1
    assert jack.primary2_classic_max == 300
    assert jack.primary2_burning_crusade_level == None
    assert jack.primary2_burning_crusade_max == None
    assert jack.primary2_wrath_of_the_lich_king_level == None
    assert jack.primary2_wrath_of_the_lich_king_max == None
    assert jack.primary2_cataclysm_level == None
    assert jack.primary2_cataclysm_max == None
    assert jack.primary2_mists_of_pandaria_level == None
    assert jack.primary2_mists_of_pandaria_max == None
    assert jack.primary2_warlords_of_draenor_level == None
    assert jack.primary2_warlords_of_draenor_max == None
    assert jack.primary2_legion_level == None
    assert jack.primary2_legion_max == None
    assert jack.primary2_battle_for_azeroth_level == None
    assert jack.primary2_battle_for_azeroth_max == None

def test_professions_clear_old_data():
    jack = Character('jack')
    response = { 'professions' :
            { 'primary' : [
                { 'id' : 182, 'name' : "Herbalism", 'icon' : 'trade_herbalism', 'rank' : 150, 'max' : 300 },
                { 'id' : 186, 'name' : "Mining", 'icon' : 'inv_pick_02', 'rank' : 122, 'max' : 300 }
            ],
            'secondary' : [
                { 'id' : 356, 'name' : "Fishing", 'icon' : 'trade_fishing', 'rank' : 0, 'max' : 300 },
                { 'id' : 185, 'name' : "Cooking", 'icon' : 'inv_misc_food_15', 'rank' : 0, 'max' : 300 },
                { 'id' : 794, 'name' : "Archaeology", 'icon' : 'trade_archaeology', 'rank' : 0, 'max' : 950 }
            ]}}

    jack.primary1_name = 'Tailoring'
    jack.primary1_icon = 'trade_tailoring'
    jack.primary1_classic_level = 1
    jack.priamry1_classic_max = 300
    jack.primary1_burning_crusade_level = 1
    jack.priamry1_burning_crusade_max = 75

    Section.professions(jack, response)

    assert jack.primary1_name == 'Herbalism'
    assert jack.primary1_icon == 'trade_herbalism'
    assert jack.primary1_classic_level == 150
    assert jack.primary1_classic_max == 300
    assert jack.primary1_burning_crusade_level == None
    assert jack.primary1_burning_crusade_max == None
