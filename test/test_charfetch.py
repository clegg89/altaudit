#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for charfetch.py
"""
import pytest
from unittest.mock import patch

import datetime
import pickle
import os
import io

from charfetch.charfetch import *

classes_raw = {'classes': [
    {'id': 1, 'mask': 1, 'powerType': 'rage', 'name': 'Warrior'},
    {'id': 2, 'mask': 2, 'powerType': 'mana', 'name': 'Paladin'},
    {'id': 3, 'mask': 4, 'powerType': 'focus', 'name': 'Hunter'},
    {'id': 4, 'mask': 8, 'powerType': 'energy', 'name': 'Rogue'},
    {'id': 5, 'mask': 16, 'powerType': 'mana', 'name': 'Priest'},
    {'id': 6, 'mask': 32, 'powerType': 'runic-power', 'name': 'Death Knight'},
    {'id': 7, 'mask': 64, 'powerType': 'mana', 'name': 'Shaman'},
    {'id': 8, 'mask': 128, 'powerType': 'mana', 'name': 'Mage'},
    {'id': 9, 'mask': 256, 'powerType': 'mana', 'name': 'Warlock'},
    {'id': 10, 'mask': 512, 'powerType': 'energy', 'name': 'Monk'},
    {'id': 11, 'mask': 1024, 'powerType': 'mana', 'name': 'Druid'},
    {'id': 12, 'mask': 2048, 'powerType': 'fury', 'name': 'Demon Hunter'}]}

races_raw = {'races': [
    {'id': 1, 'mask': 1, 'side': 'alliance', 'name': 'Human'},
    {'id': 2, 'mask': 2, 'side': 'horde', 'name': 'Orc'},
    {'id': 3, 'mask': 4, 'side': 'alliance', 'name': 'Dwarf'},
    {'id': 4, 'mask': 8, 'side': 'alliance', 'name': 'Night Elf'},
    {'id': 5, 'mask': 16, 'side': 'horde', 'name': 'Undead'},
    {'id': 6, 'mask': 32, 'side': 'horde', 'name': 'Tauren'},
    {'id': 7, 'mask': 64, 'side': 'alliance', 'name': 'Gnome'},
    {'id': 8, 'mask': 128, 'side': 'horde', 'name': 'Troll'},
    {'id': 9, 'mask': 256, 'side': 'horde', 'name': 'Goblin'},
    {'id': 10, 'mask': 512, 'side': 'horde', 'name': 'Blood Elf'},
    {'id': 11, 'mask': 1024, 'side': 'alliance', 'name': 'Draenei'},
    {'id': 22, 'mask': 2097152, 'side': 'alliance', 'name': 'Worgen'},
    {'id': 24, 'mask': 8388608, 'side': 'neutral', 'name': 'Pandaren'},
    {'id': 25, 'mask': 16777216, 'side': 'alliance', 'name': 'Pandaren'},
    {'id': 26, 'mask': 33554432, 'side': 'horde', 'name': 'Pandaren'},
    {'id': 27, 'mask': 67108864, 'side': 'horde', 'name': 'Nightborne'},
    {'id': 28, 'mask': 134217728, 'side': 'horde', 'name': 'Highmountain Tauren'},
    {'id': 29, 'mask': 268435456, 'side': 'alliance', 'name': 'Void Elf'},
    {'id': 30, 'mask': 536870912, 'side': 'alliance', 'name': 'Lightforged Draenei'},
    {'id': 31, 'mask': 1073741824, 'side': 'horde', 'name': 'Zandalari Troll'},
    {'id': 32, 'mask': -2147483648, 'side': 'alliance', 'name': 'Kul Tiran'},
    {'id': 34, 'mask': 2, 'side': 'alliance', 'name': 'Dark Iron Dwarf'},
    {'id': 36, 'mask': 8, 'side': 'horde', 'name': "Mag'har Orc"}]}

classes = {
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

races = {
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

test_dir = os.path.dirname(os.path.realpath(__file__))

with open(test_dir + '/clegg.pkl', 'rb') as f:
    character_data = pickle.load(f)

with open(test_dir + '/minitru.pkl', 'rb') as f:
    other_character_data = pickle.load(f)

character = { 'name' : 'clegg', 'realm' : "kil'jaeden", 'region' : 'us' }
other_character = { 'name' : 'minitru', 'realm' : 'lightbringer', 'region' : 'us' }

def exploding_fake():
    assert False

@pytest.fixture
def fake_char():
    return {'name' : 'toon1', 'realm' : "kil'jaeden", 'region' : 'us'}

@pytest.fixture
def fake_api():
    class FakeWowApi:
        def __init__(self):
            self.return_value = None
            self.last_region = None
            self.last_realm = None
            self.last_name = None
            self.last_filters = None

        def get_character_profile(self, region, realm, name, **filters):
            self.last_region = region
            self.last_realm = realm
            self.last_name = name
            self.last_filters = filters

            return self.return_value

        def get_character_classes(self, region, **filters):
            self.last_region = region
            self.last_filters = filters

            return classes_raw

        def get_character_races(self, region, **filters):
            self.last_region = region
            self.last_filters = filters

            return races_raw

    return FakeWowApi()

def test_convert_to_char_list_Invalid_returns_None():
    garbage = {'a' : 2}
    assert convert_to_char_list(garbage) == None

def test_get_char_profile_None():
    assert get_char_profile(None, None) == None

def test_get_char_profile_API_None():
    assert get_char_profile('garbage', None) == None

def test_get_char_profile_Character_None():
    assert get_char_profile(None, 'Garbage') == None

def test_get_char_profile_Valid(fake_char, fake_api):
    fake_api.return_value = 'test passed'
    result = get_char_profile(fake_char, fake_api)
    assert fake_api.last_region == fake_char['region']
    assert fake_api.last_realm == fake_char['realm']
    assert fake_api.last_name == fake_char['name']
    assert result == 'test passed'

def test_get_char_profile_Valid_Filters(fake_char, fake_api):
    get_char_profile(fake_char, fake_api, locale='en_US', fields='talents,items')
    assert fake_api.last_filters == {'locale' : 'en_US', 'fields' : 'talents,items'}

def test_get_classes_None():
    assert get_classes(None) == None

def test_get_classes_Valid(fake_api):
    result = get_classes(fake_api)
    assert fake_api.last_region == 'us'
    assert result == classes

def test_get_races_None():
    assert get_races(None) == None

def test_get_races_Valid(fake_api):
    result = get_races(fake_api)
    assert fake_api.last_region == 'us'
    assert result == races

def test_load_or_fetch_Use_Stored():
    test_file = 'test.pkl'
    stored_time = datetime.datetime.now()
    load_time = stored_time + datetime.timedelta(hours=1)

    expected_result = { 'a' : 1, 'b' : 2 }
    expected_stored = { 'timestamp' : stored_time, 'data' : expected_result }

    with open(test_file, 'wb') as tf:
        pickle.dump(expected_stored, tf, pickle.HIGHEST_PROTOCOL)

    result = load_or_fetch(test_file, exploding_fake, load_time)

    with open(test_file, 'rb') as tf:
        stored = pickle.load(tf)

    os.remove(test_file)

    assert result == expected_result
    assert stored == expected_stored

def test_load_or_fetch_Fetch():
    test_file = 'test.pkl'
    stored_time = datetime.datetime.now()
    load_time = stored_time + datetime.timedelta(days=1)

    fetch_result = { 'a' : 3, 'b' : 4 }
    fake_fetch = lambda: fetch_result

    stored = { 'timestamp' : stored_time, 'data' : { 'a' : 1, 'b' : 2 } }
    expected_saved = { 'timestamp' : load_time, 'data' : fetch_result }

    with open(test_file, 'wb') as tf:
        pickle.dump(stored, tf, pickle.HIGHEST_PROTOCOL)

    result = load_or_fetch(test_file, fake_fetch, load_time)

    with open(test_file, 'rb') as tf:
        saved = pickle.load(tf)

    os.remove(test_file)

    assert result == fetch_result
    assert saved == expected_saved

def test_load_or_fetch_Fetch_File_Not_Created():
    test_file = 'test.pkl'
    load_time = datetime.datetime.now()

    fetch_result = { 'a' : 3, 'b' : 4 }
    fake_fetch = lambda: fetch_result

    expected_saved = { 'timestamp' : load_time, 'data' : fetch_result }

    result = load_or_fetch(test_file, fake_fetch, load_time)

    with open(test_file, 'rb') as tf:
        saved = pickle.load(tf)

    os.remove(test_file)

    assert result == fetch_result
    assert saved == expected_saved

def test_get_all_info_Entry0_3(fake_api):
    fake_api.return_value = character_data
    result = get_all_info(character, fake_api, datetime.datetime.now())
    assert result[0].lower() == character['name'].lower()
    assert result[1].lower() == character['region'].lower()
    assert result[2].lower() == character['realm'].lower()

def test_get_all_info_Entries_Class_Lvl_Spec_Faction_Gender_Race(fake_api):
    fake_api.return_value = character_data
    result = get_all_info(character, fake_api, datetime.datetime.now())
    assert result[3] == 'Warlock'
    assert result[4] == 120
    assert result[5] == 'Affliction'
    assert result[6] == 'Horde'
    assert result[7] == 'Male'
    assert result[8] == 'Undead'

def test_get_all_info_Entries_Class_Lvl_Spec_Faction_Gender_Race_Other_Character(fake_api):
    fake_api.return_value = other_character_data
    result = get_all_info(character, fake_api, datetime.datetime.now())
    assert result[3] == 'Priest'
    assert result[4] == 120
    assert result[5] == 'Shadow'
    assert result[6] == 'Alliance'
    assert result[7] == 'Female'
    assert result[8] == 'Lightforged Draenei'
