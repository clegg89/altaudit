#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for main charfetch entry point
"""
import pytest

import charfetch

@pytest.fixture
def mock_load_or_fetch(mocker):
    def _mock_load_or_fetch(fileName, fetcher, now, *args, **kwargs):
        if fileName == 'classes.pkl':
            return 'Classes'
        elif fileName == 'races.pkl':
            return 'Races'
        else:
            raise Exception('load_or_fetch called with unrecognized file: {}'.format(fileName))

    fake = mocker.patch('charfetch.charfetch.load_or_fetch')
    fake.side_effect = _mock_load_or_fetch

    return fake

def test_mock_load_or_fetch_classes(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('classes.pkl', 'A', 'B')
    mock_load_or_fetch.assert_called_once_with('classes.pkl', 'A', 'B')
    assert result == 'Classes'

def test_mock_load_or_fetch_races(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('races.pkl', 'A', 'B')
    mock_load_or_fetch.assert_called_once_with('races.pkl', 'A', 'B')
    assert result == 'Races'

def test_mock_load_or_fetch_unknown(mock_load_or_fetch):
    with pytest.raises(Exception):
        result = charfetch.charfetch.mock_load_or_fetch('unknown.pkl', 'C', 'D')

def test_mock_load_or_fetch_args_kwargs(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('classes.pkl', 'A', 'B', 'test', var1='other')
    mock_load_or_fetch.assert_called_once_with('classes.pkl', 'A', 'B', 'test', var1='other')

@pytest.fixture
def mock_get_char_data(mocker):
    return mocker.patch('charfetch.charfetch.get_char_data')

@pytest.fixture
def mock_get_basic_info(mocker):
    return mocker.patch('charfetch.charfetch.get_basic_info')

@pytest.fixture
def mock_get_all_items(mocker):
    return mocker.patch('charfetch.charfetch.get_all_items')

def test_internal_get_all_character_info(mock_load_or_fetch, mock_get_char_data, mock_get_basic_info, mock_get_all_items, mocker):
    mock_get_char_data.return_value = { 'items' : 'Items' }
    mock_get_basic_info.return_value = ['Basic', 'Info']
    mock_get_all_items.return_value = ['All', 'Items']
    character = {'region' : 'us'}
    expected_result = ['Basic', 'Info', 'All', 'Items']

    result = charfetch.charfetch._get_all_character_info(character, 'Now', 'Blizzard_API')

    mock_load_or_fetch.assert_has_calls(
            [mocker.call('classes.pkl', charfetch.charfetch.get_classes, 'Now', 'Blizzard_API'),
                mocker.call('races.pkl', charfetch.charfetch.get_races, 'Now', 'Blizzard_API')],
            any_order=True)
    mock_get_char_data.assert_called_once_with(character, 'Blizzard_API')
    mock_get_basic_info.assert_called_once_with(mock_get_char_data.return_value, 'Classes', 'Races', 'us')
    mock_get_all_items.assert_called_once_with('Items')
    assert result == expected_result

@pytest.fixture
def fake_token_file():
    return 'fake_tokens.yaml'

@pytest.fixture
def fake_characters_file():
    return 'fake_characters.yaml'

@pytest.fixture
def fake_tokens():
    return { 'blizzard' : { 'client_id' : 'CLIENT_ID', 'client_secret' : 'CLIENT_SECRET' } }

@pytest.fixture
def fake_load_yaml(mocker, fake_token_file, fake_characters_file, fake_tokens, fake_char_yaml):
    def _fake_load(fileName):
        if fileName == fake_token_file:
            return fake_tokens
        elif fileName == fake_characters_file:
            return fake_char_yaml
        else:
            raise Exception('load_yaml_file called with unrecognized file: {}'.format(fileName))

    fake = mocker.patch('charfetch.charfetch.load_yaml_file')
    fake.side_effect = _fake_load

    return fake

def test_fake_load_yaml_tokens(fake_load_yaml, fake_token_file, fake_tokens):
    result = charfetch.charfetch.load_yaml_file(fake_token_file)

    fake_load_yaml.assert_called_once_with(fake_token_file)
    assert result == fake_tokens

def test_fake_load_yaml_characters(fake_load_yaml, fake_characters_file, fake_char_yaml):
    result = charfetch.charfetch.load_yaml_file(fake_characters_file)

    fake_load_yaml.assert_called_once_with(fake_characters_file)
    assert result == fake_char_yaml

def test_fake_load_yaml_unknown(fake_load_yaml):
    with pytest.raises(Exception):
        result = charfetch.charfetch.load_yaml_file('unknown.yaml')

@pytest.fixture
def mock_blizzard_api(mocker):
    return mocker.patch('charfetch.charfetch.WowApi')

def test_mock_blizzard_api(mock_blizzard_api):
    mock_blizzard_api.return_value = 'Test Passed'
    result = charfetch.charfetch.WowApi('TEST_CLIENT_ID', 'TEST_CLIENT_SECRET')
    mock_blizzard_api.assert_called_once_with('TEST_CLIENT_ID', 'TEST_CLIENT_SECRET')
    assert result == 'Test Passed'

def test_charfetch_create_blizzard_api(mock_blizzard_api, fake_load_yaml, fake_token_file, fake_characters_file, fake_tokens):
    charfetch.fetch_all(fake_token_file, fake_characters_file)
    mock_blizzard_api.assert_called_once_with(fake_tokens['blizzard']['client_id'], fake_tokens['blizzard']['client_secret'])
