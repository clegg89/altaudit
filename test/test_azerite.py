#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit tests for character Azerite info
"""
import pytest

from altaudit import get_azerite_info
from altaudit.character import _get_trait_info, _get_item_traits, _get_azerite_item_info

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

def test_get_item_traits_no_azerite_empowered():
    item = { 'id' : 165513, 'azeriteEmpoweredItem' : { 'azeritePowers' : [] } }

    result = _get_item_traits(item, None, None)

    expected = []

    assert result == expected

@pytest.fixture
def fake_azerite_item_class_powers():
    return { 'azeriteClassPowers' : {
            '5': [
                {'id': 560, 'tier': 3, 'spellId': 288802},
                {'id': 113, 'tier': 3, 'spellId': 272775},
                {'id': 114, 'tier': 3, 'spellId': 272780},
                {'id': 115, 'tier': 3, 'spellId': 272788},
                {'id': 30, 'tier': 2, 'spellId': 266180},
                {'id': 102, 'tier': 2, 'spellId': 267892},
                {'id': 42, 'tier': 2, 'spellId': 267883},
                {'id': 204, 'tier': 1, 'spellId': 274366},
                {'id': 15, 'tier': 1, 'spellId': 263962},
                {'id': 13, 'tier': 0, 'spellId': 263978},
                {'id': 227, 'tier': 4, 'spellId': 275541},
                {'id': 164, 'tier': 4, 'spellId': 273307},
                {'id': 228, 'tier': 4, 'spellId': 275602},
                {'id': 165, 'tier': 4, 'spellId': 273313},
                {'id': 236, 'tier': 4, 'spellId': 275722},
                {'id': 166, 'tier': 4, 'spellId': 288340}],
            '8': [
                {'id': 560, 'tier': 3, 'spellId': 288802},
                {'id': 127, 'tier': 3, 'spellId': 286027},
                {'id': 128, 'tier': 3, 'spellId': 272932},
                {'id': 132, 'tier': 3, 'spellId': 272968},
                {'id': 30, 'tier': 2, 'spellId': 266180},
                {'id': 461, 'tier': 2, 'spellId': 279926},
                {'id': 21, 'tier': 2, 'spellId': 263984},
                {'id': 205, 'tier': 1, 'spellId': 274379},
                {'id': 15, 'tier': 1, 'spellId': 263962},
                {'id': 13, 'tier': 0, 'spellId': 263978},
                {'id': 214, 'tier': 4, 'spellId': 274594},
                {'id': 167, 'tier': 4, 'spellId': 273326},
                {'id': 215, 'tier': 4, 'spellId': 274596},
                {'id': 168, 'tier': 4, 'spellId': 288755},
                {'id': 225, 'tier': 4, 'spellId': 279854},
                {'id': 170, 'tier': 4, 'spellId': 288164}],
            '9': [
                {'id': 560, 'tier': 3, 'spellId': 288802},
                {'id': 123, 'tier': 3, 'spellId': 272891},
                {'id': 130, 'tier': 3, 'spellId': 272944},
                {'id': 131, 'tier': 3, 'spellId': 287637},
                {'id': 30, 'tier': 2, 'spellId': 266180},
                {'id': 461, 'tier': 2, 'spellId': 279926},
                {'id': 21, 'tier': 2, 'spellId': 263984},
                {'id': 208, 'tier': 1, 'spellId': 274418},
                {'id': 15, 'tier': 1, 'spellId': 263962},
                {'id': 13, 'tier': 0, 'spellId': 263978},
                {'id': 230, 'tier': 4, 'spellId': 275372},
                {'id': 183, 'tier': 4, 'spellId': 273521},
                {'id': 231, 'tier': 4, 'spellId': 275395},
                {'id': 190, 'tier': 4, 'spellId': 273523},
                {'id': 232, 'tier': 4, 'spellId': 275425},
                {'id': 460, 'tier': 4, 'spellId': 279909}]}}

def test_get_item_return_list_of_class_traits(mock_api, fake_azerite_item_class_powers):
    item = { 'id' : 165822,
             'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 13, 'tier': 0, 'spellId': 263978},
                 {'id': 15, 'tier': 1, 'spellId': 263962},
                 {'id': 30, 'tier': 2, 'spellId': 266180},
                 {'id': 123, 'tier': 3, 'spellId': 272891},
                 {'id': 183, 'tier': 4, 'spellId': 273521}]}}

    mock_api.get_item.return_value = fake_azerite_item_class_powers

    result = _get_item_traits(item, 9, mock_api)

    mock_api.get_item.assert_called_once_with('us', item['id'])
    assert result == mock_api.get_item.return_value['azeriteClassPowers']['9']

def test_get_item_use_region(mock_api, fake_azerite_item_class_powers):
    item = { 'id' : 165822,
             'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 13, 'tier': 0, 'spellId': 263978},
                 {'id': 15, 'tier': 1, 'spellId': 263962},
                 {'id': 30, 'tier': 2, 'spellId': 266180},
                 {'id': 123, 'tier': 3, 'spellId': 272891},
                 {'id': 183, 'tier': 4, 'spellId': 273521}]}}

    mock_api.get_item.return_value = fake_azerite_item_class_powers

    result = _get_item_traits(item, 9, mock_api, 'eu')

    mock_api.get_item.assert_called_once_with('eu', item['id'])

@pytest.fixture
def empty_azerite_item():
    return [
            [None, None], # tier 0
            [None, None], # tier 1
            [None, None], # tier 2
            [None, None], # tier 3
            [None, None]] # tier 4

def test_get_azerite_item_info_no_traits(empty_azerite_item):
    expected_result = empty_azerite_item

    result = _get_azerite_item_info({ 'azeriteEmpoweredItem' : { 'azeritePowers' : [] } }, 9, None)

    assert result == expected_result

@pytest.fixture
def mock_get_trait_info(mocker):
    def _fake_get_trait_info(trait, api, region='us'):
        return str(trait['id'])

    mock = mocker.patch('altaudit.character._get_trait_info')
    mock.side_effect = _fake_get_trait_info

    return mock

@pytest.fixture
def mock_get_item_traits(mocker, fake_azerite_item_class_powers):
    mock = mocker.patch('altaudit.character._get_item_traits')
    mock.return_value = fake_azerite_item_class_powers['azeriteClassPowers']['9']

    return mock

def test_get_azerite_item_info_traits(mock_api, mock_get_item_traits, mock_get_trait_info):
    item = { 'id' : 165822,
             'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 13, 'tier': 0, 'spellId': 263978},
                 {'id': 15, 'tier': 1, 'spellId': 263962},
                 {'id': 30, 'tier': 2, 'spellId': 266180},
                 {'id': 123, 'tier': 3, 'spellId': 272891},
                 {'id': 183, 'tier': 4, 'spellId': 273521}]}}

    expected_result = [
            ['13','13'],
            ['208|15','15'],
            ['30|461|21','30'],
            ['560|123|130|131','123'],
            ['230|183|231|190|232|460','183']]

    result = _get_azerite_item_info(item, 9, mock_api, 'eu')

    assert result == expected_result
    mock_get_item_traits.assert_called_once_with(item, 9, mock_api, 'eu')

def test_get_azerite_info_no_neck_is_empty(empty_azerite_item):
    expected_result = [
            None,               # HoA Level
            None,               # Azerite Exp
            None,               # Azerite Exp Remaining
            None,               # AP This week
            empty_azerite_item, # Head
            empty_azerite_item, # Shoulder
            empty_azerite_item] # Chest

    result = get_azerite_info({}, 9, None)

    assert result == expected_result

def test_get_azerite_info_neck_no_azerite_items(empty_azerite_item):
    expected_result = [
            50,               # HoA Level
            1237,               # Azerite Exp
            7321,               # Azerite Exp Remaining
            None,               # AP This week
            empty_azerite_item, # Head
            empty_azerite_item, # Shoulder
            empty_azerite_item] # Chest

    result = get_azerite_info({'neck' : {
        'quality' : 6,
        'azeriteItem' : {
            'azeriteLevel' : 50,
            'azeriteExperience' : 1237,
            'azeriteExperienceRemaining' : 7321 }}}, 9, None)

    assert result == expected_result

@pytest.fixture
def mock_get_azerite_item_info(mocker):
     mock = mocker.patch('altaudit.character._get_azerite_item_info')
     mock.return_value = [
            ['13','13'],
            ['208|15','15'],
            ['30|461|21','30'],
            ['560|123|130|131','123'],
            ['230|183|231|190|232|460','183']]

     return mock

def test_get_azerite_info_azerite_item(mock_get_azerite_item_info, empty_azerite_item, mock_api):
    expected_result = [
            None,               # HoA Level
            None,               # Azerite Exp
            None,               # Azerite Exp Remaining
            None,               # AP This week
            mock_get_azerite_item_info.return_value, # Head
            empty_azerite_item, # Shoulder
            empty_azerite_item] # Chest

    result = get_azerite_info({'head' : { 'id' : 10 }}, 9, mock_api, 'eu')

    assert result == expected_result
    mock_get_azerite_item_info.assert_called_once_with({'id' : 10}, 9, mock_api, 'eu')
