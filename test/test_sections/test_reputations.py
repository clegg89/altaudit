"""Unit Tests for Reputation info"""
import pytest

from altaudit.models import Character

import altaudit.sections as Section

def test_reputation_proudmoore():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2160, 'name' : "Proudmoore Admiralty", 'standing' : 7, 'value' : 0, 'max' : 0}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[0] == '2160+Proudmoore Admiralty+7+0+0'

def test_reputation_zandalari():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2103, 'name' : "Zandalari Empire", 'standing' : 7, 'value' : 0, 'max' : 0}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[0] == '2103+Zandalari Empire+7+0+0'

def test_reputation_storms_wake():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2162, 'name' : "Storm's Wake", 'standing' : 5, 'value' : 6565, 'max' : 12000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[1] == "2162+Storm's Wake+5+6565+12000"

def test_reputation_talanjis_expedition():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2156, 'name' : "Talanji's Expedition", 'standing' : 5, 'value' : 3830, 'max' : 12000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[1] == "2156+Talanji's Expedition+5+3830+12000"

def test_reputation_order_of_embers():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2161, 'name' : "Order of Embers", 'standing' : 5, 'value' : 8389, 'max' : 12000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[2] == "2161+Order of Embers+5+8389+12000"

def test_reputation_voldunai():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2158, 'name' : "Voldunai", 'standing' : 4, 'value' : 3450, 'max' : 6000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[2] == "2158+Voldunai+4+3450+6000"

def test_reputation_7th_legion():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2159, 'name' : "7th Legion", 'standing' : 6, 'value' : 379, 'max' : 21000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[3] == "2159+7th Legion+6+379+21000"

def test_reputation_honorbound():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2157, 'name' : "The Honorbound", 'standing' : 6, 'value' : 20347, 'max' : 21000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[3] == "2157+The Honorbound+6+20347+21000"

def test_reputation_champions_of_azeroth_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2164, 'name' : "Champions of Azeroth", 'standing' : 5, 'value' : 7897, 'max' : 12000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[4] == "2164+Champions of Azeroth+5+7897+12000"

def test_reputation_champions_of_azeroth_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2164, 'name' : "Champions of Azeroth", 'standing' : 5, 'value' : 3275, 'max' : 12000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[4] == "2164+Champions of Azeroth+5+3275+12000"

def test_reputation_tortollan_seekers_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2163, 'name' : "Tortollan Seekers", 'standing' : 4, 'value' : 162, 'max' : 6000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[5] == "2163+Tortollan Seekers+4+162+6000"

def test_reputation_tortollan_seekers_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2163, 'name' : "Tortollan Seekers", 'standing' : 4, 'value' : 4592, 'max' : 6000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[5] == "2163+Tortollan Seekers+4+4592+6000"

def test_reputation_waveblade_ankoan():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2400, 'name' : "Waveblade Ankoan", 'standing' : 3, 'value' : 75, 'max' : 3000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[6] == "2400+Waveblade Ankoan+3+75+3000"

def test_reputation_unshackled():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2373, 'name' : "The Unshackled", 'standing' : 4, 'value' : 972, 'max' : 6000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[6] == "2373+The Unshackled+4+972+6000"

def test_reputation_rustbolt_resistance_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputation' : [
        {'id' : 2391, 'name' : "Rustbolt Resistance", 'standing' : 3, 'value' : 100, 'max' : 3000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[7] == "2391+Rustbolt Resistance+3+100+3000"

def test_reputation_rustbolt_resistance_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputation' : [
        {'id' : 2391, 'name' : "Rustbolt Resistance", 'standing' : 6, 'value' : 57, 'max' : 21000}]}

    Section.reputations(jack, response)

    assert jack.reputations.split('|')[7] == "2391+Rustbolt Resistance+6+57+21000"
