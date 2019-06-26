#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit tests for character Azerite info
"""
import pytest

from charfetch import get_azerite_info
from charfetch.character import _get_trait_info

def test_get_trait_info_None():
    result = _get_trait_info(None, None)
    assert result == None

def test_get_trait_info_valid(mock_api):
    ID = 15
    spellId = 263962
    name = 'Resounding Protection'
    icon = 'ability_vehicle_shellshieldgenerator_green'
    trait = { 'id' : ID, 'tier' : 1, 'spellId' : spellId, 'bonusListId' : 0 }

    mock_api.get_spell.return_value = {'id' : spellId, 'name' : name, 'icon' : icon, 'description' : 'This is a description', 'castTime' : 'Passive' }

    expected = '{}+{}+{}+{}'.format(ID, spellId, name, icon)

    result = _get_trait_info(trait, mock_api)

    mock_api.get_spell.assert_called_once_with('us', spellId)

    assert result == expected

def test_get_trait_info_use_given_region(mock_api):
    ID = 114
    spellId = 272780
    name = 'Permeating Glow'
    icon = 'spell_holy_flashheal'
    trait = { 'id' : ID, 'tier' : 3, 'spellId' : spellId, 'bonusListId' : 0 }

    mock_api.get_spell.return_value = {'id' : spellId, 'name' : name, 'icon' : icon, 'description' : 'This is a description', 'castTime' : 'Passive' }

    expected = '{}+{}+{}+{}'.format(ID, spellId, name, icon)

    result = _get_trait_info(trait, mock_api, 'eu')

    mock_api.get_spell.assert_called_once_with('eu', spellId)

    assert result == expected

@pytest.mark.skip
def test_get_azerite_info_no_neck_is_empty():
    result = get_azerite_info({})
    assert result == [None, None, None, None,
            [[],[],[],[],[]],
            [],
            []]
