#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for Reputations
"""
import pytest

from charfetch import get_reputation_info

def test_reputation_info_proudmoore():
    data = [{'id' : 2160, 'name' : "Proudmoore Admiralty", 'standing' : 7, 'value' : 0, 'max' : 0}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[0] == '2160+Proudmoore Admiralty+7+0+0'

def test_reputation_info_zandalari():
    data = [{'id' : 2103, 'name' : "Zandalari Empire", 'standing' : 7, 'value' : 0, 'max' : 0}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[0] == '2103+Zandalari Empire+7+0+0'

def test_reputation_info_storms_wake():
    data = [{'id' : 2162, 'name' : "Storm's Wake", 'standing' : 5, 'value' : 6565, 'max' : 12000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[1] == "2162+Storm's Wake+5+6565+12000"
