#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
Common fixtures for unit tests
"""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_api():
    return MagicMock()

@pytest.fixture(scope="module")
def make_fake_char_dict():
    def _make_fake_char_dict(v):
        return { 'name' : 'toon{}'.format(v),
                 'realm' : 'realm{}'.format(v),
                 'region' : 'region{}'.format(v) }

    return _make_fake_char_dict

@pytest.fixture
def fake_char_yaml():
    return { 'us' : { "kil'jaeden" : ['toon1','toon2'], 'lightbringer' : ['toon3', 'toon4'] } }
