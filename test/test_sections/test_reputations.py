"""Unit Tests for Reputation info"""
import pytest

from altaudit.models import Character

import altaudit.sections.reputations as Section

def test_reputation_proudmoore():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Proudmoore Admiralty",
                'id' : 2160 },
            'standing' : {
                'value' : 0,
                'max' : 0,
                'name' : 'Exalted'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[0] == '2160+Proudmoore Admiralty+Exalted+0+0'

def test_reputation_zandalari():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Zandalari Empire",
                'id' : 2103 },
            'standing' : {
                'value' : 0,
                'max' : 0,
                'name' : 'Exalted'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[0] == '2103+Zandalari Empire+Exalted+0+0'

def test_reputation_storms_wake():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Storm's Wake",
                'id' : 2162 },
            'standing' : {
                'value' : 6565,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[1] == "2162+Storm's Wake+Honored+6565+12000"

def test_reputation_talanjis_expedition():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Talanji's Expedition",
                'id' : 2156 },
            'standing' : {
                'value' : 3830,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[1] == "2156+Talanji's Expedition+Honored+3830+12000"

def test_reputation_order_of_embers():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Order of Embers",
                'id' : 2161 },
            'standing' : {
                'value' : 8389,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[2] == "2161+Order of Embers+Honored+8389+12000"

def test_reputation_voldunai():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Voldunai",
                'id' : 2158 },
            'standing' : {
                'value' : 3450,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[2] == "2158+Voldunai+Friendly+3450+6000"

def test_reputation_7th_legion():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "7th Legion",
                'id' : 2159 },
            'standing' : {
                'value' : 379,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[3] == "2159+7th Legion+Revered+379+21000"

def test_reputation_honorbound():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Honorbound",
                'id' : 2157 },
            'standing' : {
                'value' : 20347,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[3] == "2157+The Honorbound+Revered+20347+21000"

def test_reputation_champions_of_azeroth_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Champions of Azeroth",
                'id' : 2164 },
            'standing' : {
                'value' : 7897,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[4] == "2164+Champions of Azeroth+Honored+7897+12000"

def test_reputation_champions_of_azeroth_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Champions of Azeroth",
                'id' : 2164 },
            'standing' : {
                'value' : 3275,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[4] == "2164+Champions of Azeroth+Honored+3275+12000"

def test_reputation_tortollan_seekers_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Tortollan Seekers",
                'id' : 2163 },
            'standing' : {
                'value' : 162,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[5] == "2163+Tortollan Seekers+Friendly+162+6000"

def test_reputation_tortollan_seekers_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Tortollan Seekers",
                'id' : 2163 },
            'standing' : {
                'value' : 4592,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[5] == "2163+Tortollan Seekers+Friendly+4592+6000"

def test_reputation_waveblade_ankoan():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Waveblade Ankoan",
                'id' : 2400 },
            'standing' : {
                'value' : 75,
                'max' : 3000,
                'name' : 'Neutral'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[6] == "2400+Waveblade Ankoan+Neutral+75+3000"

def test_reputation_unshackled():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Unshackled",
                'id' : 2373 },
            'standing' : {
                'value' : 972,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[6] == "2373+The Unshackled+Friendly+972+6000"

def test_reputation_rustbolt_resistance_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Rustbolt Resistance",
                'id' : 2391 },
            'standing' : {
                'value' : 100,
                'max' : 3000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[7] == "2391+Rustbolt Resistance+Friendly+100+3000"

def test_reputation_rustbolt_resistance_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Rustbolt Resistance",
                'id' : 2391 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[7] == "2391+Rustbolt Resistance+Revered+57+21000"

def test_reputation_no_dictionary():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : None }

    Section.reputations(jack, response, None, None)

    assert jack.reputations == None

def test_reputation_missing_key():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'id' : 2391 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations == None
