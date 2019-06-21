#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for charfetch.utility
"""
import pytest

import os

from charfetch import load_yaml_file, convert_to_char_list, flatten, get_char_data

@pytest.fixture
def fake_char_dict():
    return { 'us' : { "kil'jaeden" : ['toon1','toon2'] } }

def test_load_yaml_file_None():
    assert load_yaml_file(None) == None

def test_load_yaml_file_File(fake_char_dict):
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

def test_flatten_list():
    expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    inlist = [1, [2, [3, [4, 5, 6]], 7], [8, 9], 10]
    assert flatten(inlist) == expected_result

def test_get_char_data_blizzard_api_called(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(1)

    get_char_data(character, blizzard_api=mock_blizzard_api)

    mock_blizzard_api.get_character_profile.assert_called_once()

def test_get_char_data_blizzard_api_no_unexpected_calls(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(2)

    get_char_data(character, blizzard_api=mock_blizzard_api)

    assert len(mock_blizzard_api.method_calls) == 1, 'Unexpcted method was called'

def test_get_char_data_blizzard_api_call_args(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(3)
    expected_args = (character['region'], character['realm'], character['name'])

    get_char_data(character, blizzard_api=mock_blizzard_api)
    args, _ = mock_blizzard_api.get_character_profile.call_args

    assert args == expected_args

def test_get_char_data_blizzard_api_call_kwargs_keys_correct(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(3)

    get_char_data(character, blizzard_api=mock_blizzard_api)
    _, kwargs = mock_blizzard_api.get_character_profile.call_args

    assert list(kwargs.keys()) == ['locale', 'filters']

def test_get_char_data_blizzard_api_call_kwargs_locale_correct(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(3)

    get_char_data(character, blizzard_api=mock_blizzard_api)
    _, kwargs = mock_blizzard_api.get_character_profile.call_args

    assert kwargs['locale'] == 'en_US'

def test_get_char_data_blizzard_api_call_kwargs_filters_correct(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(3)
    expected_filters = ['achievements', 'talents', 'items', 'statistics', 'professions', 'reputation', 'audit']
    expected_filters.sort()

    get_char_data(character, blizzard_api=mock_blizzard_api)
    _, kwargs = mock_blizzard_api.get_character_profile.call_args

    filters = kwargs['filters'].split(',')
    filters.sort()

    assert filters == expected_filters

def test_get_char_data_blizzard_api_call_in_return_value(make_fake_char_dict, mock_blizzard_api):
    character = make_fake_char_dict(3)

    mock_blizzard_api.get_character_profile.return_value = 'Test Passed'
    result = get_char_data(character, blizzard_api=mock_blizzard_api)

    assert result['blizzard'] == 'Test Passed'
