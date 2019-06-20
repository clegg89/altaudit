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

from charfetch import load_yaml_file, convert_to_char_list, flatten

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
