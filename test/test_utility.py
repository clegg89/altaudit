#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for charfetch.utility
"""
import pytest

import datetime

from charfetch.utility import *

def test_flatten_list():
    expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    inlist = [1, [2, [3, [4, 5, 6]], 7], [8, 9], 10]
    assert flatten(inlist) == expected_result

@pytest.fixture
def mock_yaml(mocker):
    return mocker.patch('charfetch.utility.yaml')

def test_load_yaml_file_valid(fake_char_yaml, mock_yaml, mocker):
    test_file = 'test.yaml'

    mock_yaml.safe_load.return_value = fake_char_yaml
    m = mocker.patch('charfetch.utility.open', mocker.mock_open())
    result = load_yaml_file(test_file)

    m.assert_called_once_with(test_file, 'r')
    mock_yaml.safe_load.assert_called_once_with(m.return_value)
    assert result == fake_char_yaml

def test_load_yaml_invalid_returns_None():
    with pytest.raises(Exception):
        garbage = 'file_does_not_exist'
        load_yaml_file(garbage)

def test_load_yaml_file_None():
    with pytest.raises(Exception):
        load_yaml_file(None)

def test_convert_to_char_list_None():
    assert convert_to_char_list(None) == None

def test_convert_to_char_list_valid(fake_char_yaml):
    expected_result = [
            {'name' : 'toon1', 'realm' : "kil'jaeden", 'region' : 'us'},
            {'name' : 'toon2', 'realm' : "kil'jaeden", 'region' : 'us'},
            {'name' : 'toon3', 'realm' : "lightbringer", 'region' : 'us'},
            {'name' : 'toon4', 'realm' : "lightbringer", 'region' : 'us'}]
    assert convert_to_char_list(fake_char_yaml) == expected_result

def test_convert_to_char_list_invalid_returns_None():
    garbage = {'a' : 2}
    assert convert_to_char_list(garbage) == None

def test_get_char_data_api_no_unexpected_calls(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(2)

    get_char_data(character, blizzard_api=mock_api)

    assert len(mock_api.method_calls) == 2, 'Unexpcted method was called'

def test_get_char_data_api_character_profile_called(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(1)

    get_char_data(character, blizzard_api=mock_api)

    mock_api.get_character_profile.assert_called_once()

def test_get_char_data_api_character_profile_call_args(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(3)
    expected_args = (character['region'], character['realm'], character['name'])

    get_char_data(character, blizzard_api=mock_api)
    args, _ = mock_api.get_character_profile.call_args

    assert args == expected_args

def test_get_char_data_api_character_profile_call_kwargs_keys_correct(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(3)

    get_char_data(character, blizzard_api=mock_api)
    _, kwargs = mock_api.get_character_profile.call_args

    assert list(kwargs.keys()) == ['locale', 'fields']

def test_get_char_data_api_character_profile_call_kwargs_locale_correct(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(3)

    get_char_data(character, blizzard_api=mock_api)
    _, kwargs = mock_api.get_character_profile.call_args

    assert kwargs['locale'] == 'en_US'

def test_get_char_data_api_character_profile_call_kwargs_fields_correct(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(3)
    expected_fields = ['achievements', 'talents', 'items', 'statistics', 'professions', 'reputation', 'audit']
    expected_fields.sort()

    get_char_data(character, blizzard_api=mock_api)
    _, kwargs = mock_api.get_character_profile.call_args

    fields = kwargs['fields'].split(',')
    fields.sort()

    assert fields == expected_fields

def test_get_char_data_api_media_call_correct(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(1)

    get_char_data(character, blizzard_api=mock_api)

    mock_api.get_resource.assert_called_once_with('profile/wow/character/{0}/{1}/character-media', 'us', *[character['realm'], character['name']], locale='en_US', namespace='profile-us')

def test_get_char_data_api_call_in_return_value(make_fake_char_dict, mock_api):
    character = make_fake_char_dict(3)

    mock_api.get_character_profile.return_value = 'Test Passed'
    mock_api.get_resource.return_value = 'Other Test Passed'
    result = get_char_data(character, blizzard_api=mock_api)

    assert result['blizzard'] == {'community_profile' : 'Test Passed', 'media' : 'Other Test Passed'}

def test_get_classes_api_called_with_region(mock_api):
    get_classes(mock_api)

    mock_api.get_character_classes.assert_called_once_with('us', locale='en_US')

def test_get_classes_api_no_unexpected_calls(mock_api):
    get_classes(mock_api)

    assert len(mock_api.method_calls) == 1, 'Unexpcted method was called'

def test_get_classes_return_value_coerced(mock_api):
    classes_in = {'classes' : [
        {'id': 1, 'mask': 1, 'powerType': 'rage', 'name': 'Warrior'},
        {'id': 2, 'mask': 2, 'powerType': 'mana', 'name': 'Paladin'},
        {'id': 3, 'mask': 4, 'powerType': 'focus', 'name': 'Hunter'}]}
    expected_result = {
        1 : 'Warrior',
        2 : 'Paladin',
        3 : 'Hunter'}

    mock_api.get_character_classes.return_value = classes_in

    result = get_classes(mock_api)

    assert result == expected_result

def test_get_races_api_called_with_region(mock_api):
    get_races(mock_api)

    mock_api.get_character_races.assert_called_once_with('us', locale='en_US')

def test_get_races_api_no_unexpected_calls(mock_api):
    get_races(mock_api)

    assert len(mock_api.method_calls) == 1, 'Unexpcted method was called'

def test_get_races_return_value_coerced(mock_api):
    races_in = {'races': [
        {'id': 1, 'mask': 1, 'side': 'alliance', 'name': 'Human'},
        {'id': 2, 'mask': 2, 'side': 'horde', 'name': 'Orc'},
        {'id': 3, 'mask': 4, 'side': 'alliance', 'name': 'Dwarf'}]}
    expected_result =  {
        1 : {'side': 'alliance', 'name': 'Human'},
        2 : {'side': 'horde', 'name': 'Orc'},
        3 : {'side': 'alliance', 'name': 'Dwarf'}}

    mock_api.get_character_races.return_value = races_in

    result = get_races(mock_api)

    assert result == expected_result

@pytest.fixture
def mock_pickle(mocker):
    return mocker.patch('charfetch.utility.pickle')

# TODO refactor - lots of duplicate code in following tests

def test_load_or_fetch_use_stored_old(mock_pickle, mocker):
    test_file = 'test.pkl'
    stored_time = datetime.datetime.now()
    load_time = stored_time + datetime.timedelta(hours=1)

    expected_result = { 'a' : 1, 'b' : 2 }
    stored = { 'timestamp' : stored_time, 'data' : expected_result }

    mock_pickle.load.return_value = stored
    m = mocker.patch('charfetch.utility.open', mocker.mock_open())
    result = load_or_fetch(test_file, None, load_time)

    m.assert_called_once_with(test_file, 'rb')
    mock_pickle.load.assert_called_once_with(m.return_value)
    assert result == expected_result

def test_load_or_fetch_fetch(mock_pickle, mocker):
    test_file = 'test.pkl'
    stored_time = datetime.datetime.now()
    load_time = stored_time + datetime.timedelta(days=1)

    fetch_result = { 'a' : 3, 'b' : 4 }
    fake_fetch = lambda: fetch_result

    stored = { 'timestamp' : stored_time, 'data' : { 'a' : 1, 'b' : 2 } }
    expected_saved = { 'timestamp' : load_time, 'data' : fetch_result }

    mock_pickle.load.return_value = stored
    m = mocker.patch('charfetch.utility.open', mocker.mock_open())
    result = load_or_fetch(test_file, fake_fetch, load_time)

    mock_pickle.load.assert_called_once_with(m.return_value)
    mock_pickle.dump.assert_called_once_with(expected_saved, m.return_value, mock_pickle.HIGHEST_PROTOCOL)
    assert result == fetch_result

def test_load_or_fetch_fetch_file_not_created(mock_pickle, mocker):
    def _raise_on_read(fname, mode):
        if mode != 'wb':
            raise FileNotFoundError
        else:
            return mocker.DEFAULT

    test_file = 'test.pkl'
    load_time = datetime.datetime.now()

    fetch_result = { 'a' : 3, 'b' : 4 }
    fake_fetch = lambda: fetch_result

    expected_saved = { 'timestamp' : load_time, 'data' : fetch_result }

    m = mocker.patch('charfetch.utility.open', mocker.mock_open())
    m.side_effect = _raise_on_read
    result = load_or_fetch(test_file, fake_fetch, load_time)

    mock_pickle.load.assert_not_called()
    mock_pickle.dump.assert_called_once_with(expected_saved, m.return_value, mock_pickle.HIGHEST_PROTOCOL)
    assert result == fetch_result

def test_load_or_fetch_fetch_args_and_kwargs(mock_pickle, mocker):
    test_file = 'test.pkl'
    stored_time = datetime.datetime.now()
    load_time = stored_time + datetime.timedelta(days=1)

    mock_fetcher = mocker.MagicMock()
    args = [3, 'test']
    kwargs = {'var1' : 4, 'var3' : 'passed'}

    fetch_result = { 'a' : 3, 'b' : 4 }
    mock_fetcher.return_value = fetch_result

    stored = { 'timestamp' : stored_time, 'data' : { 'a' : 1, 'b' : 2 } }
    expected_saved = { 'timestamp' : load_time, 'data' : fetch_result }

    mock_pickle.load.return_value = stored
    m = mocker.patch('charfetch.utility.open', mocker.mock_open())
    result = load_or_fetch(test_file, mock_fetcher, load_time, *args, **kwargs)

    mock_pickle.load.assert_called_once_with(m.return_value)
    mock_fetcher.assert_called_once_with(*args, **kwargs)
    mock_pickle.dump.assert_called_once_with(expected_saved, m.return_value, mock_pickle.HIGHEST_PROTOCOL)
