#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Test the Character class
"""
import pytest

import os
import pickle
import wowapi

from charfetch.character import Character

@pytest.fixture(scope="module")
def classes():
    return  {
            1 : 'Warrior',
            2 : 'Paladin',
            3 : 'Hunter',
            4 : 'Rogue',
            5 : 'Priest',
            6 : 'Death Knight',
            7 : 'Shaman',
            8 : 'Mage',
            9 : 'Warlock',
            10 : 'Monk',
            11 : 'Druid',
            12 : 'Demon Hunter'}

@pytest.fixture(scope="module")
def races():
    return {
            1 : {'side': 'alliance', 'name': 'Human'},
            2 : {'side': 'horde', 'name': 'Orc'},
            3 : {'side': 'alliance', 'name': 'Dwarf'},
            4 : {'side': 'alliance', 'name': 'Night Elf'},
            5 : {'side': 'horde', 'name': 'Undead'},
            6 : {'side': 'horde', 'name': 'Tauren'},
            7 : {'side': 'alliance', 'name': 'Gnome'},
            8 : {'side': 'horde', 'name': 'Troll'},
            9 : {'side': 'horde', 'name': 'Goblin'},
            10 : {'side': 'horde', 'name': 'Blood Elf'},
            11 : {'side': 'alliance', 'name': 'Draenei'},
            22 : {'side': 'alliance', 'name': 'Worgen'},
            24 : {'side': 'neutral', 'name': 'Pandaren'},
            25 : {'side': 'alliance', 'name': 'Pandaren'},
            26 : {'side': 'horde', 'name': 'Pandaren'},
            27 : {'side': 'horde', 'name': 'Nightborne'},
            28 : {'side': 'horde', 'name': 'Highmountain Tauren'},
            29 : {'side': 'alliance', 'name': 'Void Elf'},
            30 : {'side': 'alliance', 'name': 'Lightforged Draenei'},
            31 : {'side': 'horde', 'name': 'Zandalari Troll'},
            32 : {'side': 'alliance', 'name': 'Kul Tiran'},
            34 : {'side': 'alliance', 'name': 'Dark Iron Dwarf'},
            36 : {'side': 'horde', 'name': "Mag'har Orc"}}

@pytest.fixture(scope="module")
def make_fake_char_dict():
    def _make_fake_char_dict(v):
        return { 'name' : 'toon{}'.format(v),
                 'realm' : 'realm{}'.format(v),
                 'region' : 'region{}'.format(v) }

    return _make_fake_char_dict

@pytest.fixture(scope="module")
def character_data():
    testdir = os.path.dirname(os.path.realpath(__file__))
    with open(testdir + '/test_toons.pkl', 'rb') as f:
        test_toons = pickle.load(f)

    return test_toons

@pytest.fixture
def mock_api(mocker):
    return mocker.patch('wowapi.WowApi').return_value

@pytest.fixture(params=[1,3,9])
def class_index(request):
    return request.param

@pytest.fixture(params=[2,22,24,25,34])
def race_index(request):
    return request.param

@pytest.fixture(params=[0,1,2])
def faction_key(request):
    return request.param

@pytest.fixture(params=[0,1])
def gender_key(request):
    return request.param

@pytest.fixture(params=[5,10,120])
def level(request):
    return request.param

@pytest.fixture(params=['Affliction','Shadow'])
def spec_fixture(request):
    spec = {}
    spec['mainspec'] = request.param
    spec['talents'] = [
            { 'selected' : True, 'spec' : { 'name' : request.param } },
            { 'selected' : False, 'spec' : { 'name' : 'Failed' } },
            { 'selected' : False, 'spec' : { 'name' : 'Failed' } }]
    for i in range(6):
        spec['talents'].append({'talents': [], 'calcTalent': '', 'calcSpec': ''})

    return spec

class TestCharacter:
    @pytest.fixture(autouse=True)
    def create_character(self, classes, races, make_fake_char_dict, mock_api):
        self.char_dict = make_fake_char_dict(0)
        self.api = mock_api
        self.classes = classes
        self.races = races
        self.character = Character(self.char_dict, self.api, classes=self.classes, races=self.races)

    def test_no_api_call_on_init(self):
        self.api.assert_not_called()
        assert not self.api.method_calls

    def test_store_dict_data(self):
        assert self.character.name ==  self.char_dict['name']
        assert self.character.realm ==  self.char_dict['realm']
        assert self.character.region ==  self.char_dict['region']

    def test_store_classes_and_races(self):
        assert self.character._classes == self.classes
        assert self.character._races == self.races

    def test_update_fetches_profile_from_api(self):
        char = self.char_dict
        args = (char['region'], char['realm'], char['name'])
        kwargs = { 'locale' : 'en_US', 'filters' : 'talents,items,statistics,professions,reputation,audit' }
        self.api.get_character_profile.return_value = 'Test Passed'
        self.character._update()
        self.api.get_character_profile.assert_called_once_with(*args, **kwargs)
        assert self.character._profile == 'Test Passed'

    def test_get_class_returns_string(self, class_index):
        self.api.get_character_profile.return_value = { 'class' : class_index }
        assert self.character.get_class() == self.classes[class_index]

    def test_get_class_fetches_classes_if_necessary(self):
        self.api.get_character_profile.return_value = { 'class' : 9 }
        self.api.get_character_classes.return_value = self.classes
        other_char = Character(self.char_dict, self.api)
        other_char.get_class()
        self.api.get_character_classes.assert_called_once_with('us')

    def test_get_race_return_string(self, race_index):
        self.api.get_character_profile.return_value = { 'race' : race_index }
        assert self.character.get_race() == self.races[race_index]['name']

    def test_get_race_fetches_races_if_necessary(self):
        self.api.get_character_profile.return_value = { 'race' : 3 }
        self.api.get_character_races.return_value = self.races
        other_char = Character(self.char_dict, self.api)
        other_char.get_race()
        self.api.get_character_races.assert_called_once_with('us')

    def test_get_factions(self, faction_key):
        factions = { 0 : 'Alliance', 1 : 'Horde', 2 : 'Neutral' }
        self.api.get_character_profile.return_value = { 'faction' : faction_key }
        assert self.character.get_faction() == factions[faction_key]

    def test_get_gender(self, gender_key):
        genders = { 0 : 'Male', 1 : 'Female' }
        self.api.get_character_profile.return_value = { 'gender' : gender_key }
        assert self.character.get_gender() == genders[gender_key]

    def test_get_level(self, level):
        self.api.get_character_profile.return_value = { 'level' : level }
        assert self.character.get_level() == level

    def test_get_mainspec(self, spec_fixture):
        self.api.get_character_profile.return_value = { 'talents' : spec_fixture['talents'] }
        assert self.character.get_mainspec() == spec_fixture['mainspec']
