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
        if fileName is fake_token_file:
            return fake_tokens
        elif fileName is fake_characters_file:
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
