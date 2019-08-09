"""Unit Tests for Profesion Info"""
import pytest

from altaudit.models import Character

import altaudit.sections as Section

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
