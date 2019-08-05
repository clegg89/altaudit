#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for Reputations
"""
import pytest

from altaudit import get_reputation_info

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

def test_reputation_info_talanjis_expedition():
    data = [{'id' : 2156, 'name' : "Talanji's Expedition", 'standing' : 5, 'value' : 3830, 'max' : 12000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[1] == "2156+Talanji's Expedition+5+3830+12000"

def test_reputation_info_order_of_embers():
    data = [{'id' : 2161, 'name' : "Order of Embers", 'standing' : 5, 'value' : 8389, 'max' : 12000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[2] == "2161+Order of Embers+5+8389+12000"

def test_reputation_info_voldunai():
    data = [{'id' : 2158, 'name' : "Voldunai", 'standing' : 4, 'value' : 3450, 'max' : 6000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[2] == "2158+Voldunai+4+3450+6000"

def test_reputation_info_7th_legion():
    data = [{'id' : 2159, 'name' : "7th Legion", 'standing' : 6, 'value' : 379, 'max' : 21000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[3] == "2159+7th Legion+6+379+21000"

def test_reputation_info_honorbound():
    data = [{'id' : 2157, 'name' : "The Honorbound", 'standing' : 6, 'value' : 20347, 'max' : 21000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[3] == "2157+The Honorbound+6+20347+21000"

def test_reputation_info_champions_of_azeroth_alliance():
    data = [{'id' : 2164, 'name' : "Champions of Azeroth", 'standing' : 5, 'value' : 7897, 'max' : 12000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[4] == "2164+Champions of Azeroth+5+7897+12000"

def test_reputation_info_champions_of_azeroth_horde():
    data = [{'id' : 2164, 'name' : "Champions of Azeroth", 'standing' : 5, 'value' : 3275, 'max' : 12000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[4] == "2164+Champions of Azeroth+5+3275+12000"

def test_reputation_info_tortollan_seekers_alliance():
    data = [{'id' : 2163, 'name' : "Tortollan Seekers", 'standing' : 4, 'value' : 162, 'max' : 6000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[5] == "2163+Tortollan Seekers+4+162+6000"

def test_reputation_info_tortollan_seekers_horde():
    data = [{'id' : 2163, 'name' : "Tortollan Seekers", 'standing' : 4, 'value' : 4592, 'max' : 6000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[5] == "2163+Tortollan Seekers+4+4592+6000"

def test_reputation_info_waveblade_ankoan():
    data = [{'id' : 2400, 'name' : "Waveblade Ankoan", 'standing' : 3, 'value' : 75, 'max' : 3000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[6] == "2400+Waveblade Ankoan+3+75+3000"

def test_reputation_info_unshackled():
    data = [{'id' : 2373, 'name' : "The Unshackled", 'standing' : 4, 'value' : 972, 'max' : 6000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[6] == "2373+The Unshackled+4+972+6000"

def test_reputation_info_rustbolt_resistance_alliance():
    data = [{'id' : 2391, 'name' : "Rustbolt Resistance", 'standing' : 3, 'value' : 100, 'max' : 3000}]

    result = get_reputation_info(data, 0)

    assert result.split('|')[7] == "2391+Rustbolt Resistance+3+100+3000"

def test_reputation_info_rustbolt_resistance_horde():
    data = [{'id' : 2391, 'name' : "Rustbolt Resistance", 'standing' : 6, 'value' : 57, 'max' : 21000}]

    result = get_reputation_info(data, 1)

    assert result.split('|')[7] == "2391+Rustbolt Resistance+6+57+21000"
