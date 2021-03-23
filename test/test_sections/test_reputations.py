"""Unit Tests for Reputation info"""
import pytest

from altaudit.models import Character

import altaudit.sections.reputations as Section

def test_reputation_the_ascended_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Ascended",
                'id' : 2407 },
            'standing' : {
                'value' : 7897,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[0] == "2407+The Ascended+Honored+7897+12000"

def test_reputation_the_ascended_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Ascended",
                'id' : 2407 },
            'standing' : {
                'value' : 3275,
                'max' : 12000,
                'name' : 'Honored'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[0] == "2407+The Ascended+Honored+3275+12000"

def test_reputation_the_undying_army_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Undying Army",
                'id' : 2410 },
            'standing' : {
                'value' : 162,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[1] == "2410+The Undying Army+Friendly+162+6000"

def test_reputation_the_undying_army_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Undying Army",
                'id' : 2410 },
            'standing' : {
                'value' : 4592,
                'max' : 6000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[1] == "2410+The Undying Army+Friendly+4592+6000"

def test_reputation_court_of_harvesters_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Court of Harvesters",
                'id' : 2413 },
            'standing' : {
                'value' : 100,
                'max' : 3000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[2] == "2413+Court of Harvesters+Friendly+100+3000"

def test_reputation_court_of_harvesters_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Court of Harvesters",
                'id' : 2413 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[2] == "2413+Court of Harvesters+Revered+57+21000"

def test_reputation_venari_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Venari",
                'id' : 2432 },
            'standing' : {
                'value' : 100,
                'max' : 3000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[3] == "2432+Venari+Friendly+100+3000"

def test_reputation_venari_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "Venari",
                'id' : 2432 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[3] == "2432+Venari+Revered+57+21000"

def test_reputation_the_avowed_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Avowed",
                'id' : 2439 },
            'standing' : {
                'value' : 100,
                'max' : 3000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[4] == "2439+The Avowed+Friendly+100+3000"

def test_reputation_the_avowed_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Avowed",
                'id' : 2439 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[4] == "2439+The Avowed+Revered+57+21000"

def test_reputation_the_wild_hunt_alliance():
    jack = Character('jack', faction_name='Alliance')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Wild Hunt",
                'id' : 2465 },
            'standing' : {
                'value' : 100,
                'max' : 3000,
                'name' : 'Friendly'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[5] == "2465+The Wild Hunt+Friendly+100+3000"

def test_reputation_the_wild_hunt_horde():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'name' : "The Wild Hunt",
                'id' : 2465 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations.split('|')[5] == "2465+The Wild Hunt+Revered+57+21000"

def test_reputation_no_dictionary():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : None }

    Section.reputations(jack, response, None, None)

    assert jack.reputations == None

def test_reputation_missing_key():
    jack = Character('jack', faction_name='Horde')
    response = { 'reputations' : { 'reputations' : [
        { 'faction' : {
                'id' : 2465 },
            'standing' : {
                'value' : 57,
                'max' : 21000,
                'name' : 'Revered'}}]}}

    Section.reputations(jack, response, None, None)

    assert jack.reputations == None
