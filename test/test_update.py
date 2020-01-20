"""Unit Tests for altaudit.update"""
import pytest

import copy

import altaudit.update as updater

def test_update_config_no_change():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando', 'randy'] } }
    expected = copy.deepcopy(config)
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_name():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando', 'randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'][0] = 'ray'
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['name'] = 'ray'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_existing():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'].append('archer')
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_new():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'] = ['archer']
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_realm_remove_empty():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    del expected['us']['lightbringer']
    expected['us']['kiljaeden'].append('randy')
    charIn = { 'name' : 'randy', 'realm' : 'lightbringer' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'kiljaeden'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected

def test_update_config_change_name_and_realm():
    config = {'us' : { 'kiljaeden' : ['archer', 'rando'], 'lightbringer' : ['randy'] } }
    expected = copy.deepcopy(config)
    expected['us']['kiljaeden'].remove('archer')
    expected['us']['lightbringer'].append('ray')
    charIn = { 'name' : 'archer', 'realm' : 'kiljaeden' }
    charOut = copy.deepcopy(charIn)
    charOut['realm'] = 'lightbringer'
    charOut['name'] = 'ray'

    updater._update_config(config, 'us', charIn, charOut)

    assert config == expected
