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
