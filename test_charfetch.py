#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 csmith <csmith@LAPTOP-RUIE9BRU>
#
# Distributed under terms of the MIT license.

"""
Unit Tests for charfetch.py
"""
import pytest

from charfetch import *

@pytest.fixture
def fake_char_dict():
    return { 'us' : { "kil'jaeden" : ['toon1','toon2'] } }

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

            return self.return_value

        def get_character_races(self, region, **filters):
            self.last_region = region
            self.last_filters = filters

            return self.return_value

    return FakeWowApi()

def test_load_yaml_file_None():
    assert load_yaml_file(None) == None

def test_load_yaml_file_File(fake_char_dict):
    import os
    test_file = 'test.yaml'
    fake_yaml = """us:
    kil'jaeden:
        - toon1
        - toon2"""
    expected_result = fake_char_dict
    with open(test_file, 'w') as f:
        f.write(fake_yaml)
    result = load_yaml_file(test_file)
    os.remove(test_file)
    assert result == expected_result

def test_load_yaml_Invalid_returns_None():
    garbage = 'file_does_not_exist'
    assert load_yaml_file(garbage) == None

def test_convert_to_char_list_None():
    assert convert_to_char_list(None) == None

def test_convert_to_char_list_Valid(fake_char_dict):
    expected_result = [
            {'name' : 'toon1', 'realm' : "kil'jaeden", 'region' : 'us'},
            {'name' : 'toon2', 'realm' : "kil'jaeden", 'region' : 'us'}]
    assert convert_to_char_list(fake_char_dict) == expected_result

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
    fake_api.return_value = {'classes' : [
        {'id' : 1, 'mask' : 1, 'powerType': 'rage', 'name' : 'Warrior'},
        {'id' : 2, 'mask' : 2, 'powerType': 'mana', 'name' : 'Paladin'}]}
    expected_result = { 1 : 'Warrior', 2 : 'Paladin' }
    result = get_classes(fake_api)
    assert fake_api.last_region == 'us'
    assert result == expected_result

def test_get_races_None():
    assert get_races(None) == None

def test_get_races_Valid(fake_api):
    fake_api.return_value = {'races' : [
        {'id' : 1, 'side' : 'alliance', 'name': 'Human'},
        {'id' : 5, 'side' : 'horde', 'name' : 'Undead'}]}
    expected_result = {
            1 : {'side' : 'alliance', 'name' : 'Human'},
            5 : {'side' : 'horde', 'name' : 'Undead'}}
    result = get_races(fake_api)
    assert fake_api.last_region == 'us'
    assert result == expected_result
