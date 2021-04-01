"""Unit Tests for covenant info"""
import pytest

from altaudit.models import Character

import altaudit.sections.covenant as Section

def test_covenant_get_covenant_data_from_profile():
    jack = Character('jack')
    response = {
            'summary' : {
                'covenant_progress' : {
                    'chosen_covenant' : {
                        'name' : 'Night Fae' },
                    'renown_level' : 40 }},
            'soulbinds' : {
                'soulbinds' : [
                    {'soulbind' : { 'name' : 'Niya' },
                     'traits' : [
                         {},
                         { 'conduit_socket' : {
                             'socket' : { 'conduit' : {
                                 'name' : "Focused Malignancy",
                                 'id' : 202},
                             'rank' : 5}}},
                         {},
                         { 'conduit_socket' : {
                             'socket' : { 'conduit' : {
                                 'name' : "Demonic Momentum",
                                 'id' : 171},
                             'rank' : 6}}},
                         {},
                         { 'conduit_socket' : {
                             'socket' : { 'conduit' : {
                                 'name' : "Diabolic Bloodstone",
                                 'id' : 222},
                             'rank' : 6}}},
                         { 'conduit_socket' : {
                             'socket' : { 'conduit' : {
                                 'name' : "Rolling Agony",
                                 'id' : 201},
                             'rank' : 7}}},
                         {}],
                     'is_active' : True},
                    {'soulbind' : { 'name' : 'Dreamweaver' }},
                    {'soulbind' : { 'name' : 'Korayn'}}]}}

    expected_conduits = [
            {
                'name' : "Focused Malignancy",
                'id'   : 202,
                'ilvl' : 200
            }, {
                'name' : "Demonic Momentum",
                'id'   : 171,
                'ilvl' : 213
            }, {
                'name' : "Diabolic Bloodstone",
                'id'   : 222,
                'ilvl' : 213
            }, {
                'name' : "Rolling Agony",
                'id'   : 201,
                'ilvl' : 226
            }]

    Section.covenant(jack, response, None)

    actual_conduits = [
            {
                'name' : jack.conduit_1_name,
                'id'   : jack.conduit_1_id,
                'ilvl' : jack.conduit_1_ilvl
            }, {
                'name' : jack.conduit_2_name,
                'id'   : jack.conduit_2_id,
                'ilvl' : jack.conduit_2_ilvl
            }, {
                'name' : jack.conduit_3_name,
                'id'   : jack.conduit_3_id,
                'ilvl' : jack.conduit_3_ilvl
            }, {
                'name' : jack.conduit_4_name,
                'id'   : jack.conduit_4_id,
                'ilvl' : jack.conduit_4_ilvl
            }]

    assert jack.covenant == 'Night Fae'
    assert jack.renown == 40
    assert jack.current_soulbind == 'Niya'
    assert expected_conduits[0] in actual_conduits, "{} not found in conduits".format(expected_conduits[0])
    assert expected_conduits[1] in actual_conduits, "{} not found in conduits".format(expected_conduits[1])
    assert expected_conduits[2] in actual_conduits, "{} not found in conduits".format(expected_conduits[2])
    assert expected_conduits[3] in actual_conduits, "{} not found in conduits".format(expected_conduits[3])

def test_covenant_no_covenant():
    jack = Character('jack')
    response = { 'summary' : {} }

    Section.covenant(jack, response, None)

    assert jack.covenant == None
    assert jack.renown == None

def test_covenant_no_chosen_covenant():
    jack = Character('jack')
    response = { 'summary' : {
        'covenant_progress' : { 'renown_level' : 30 }}}

    Section.covenant(jack, response, None)

    assert jack.covenant == None
    assert jack.renown == 30

def test_covenant_no_chosen_covenant_name():
    jack = Character('jack')
    response = { 'summary' : {
        'covenant_progress' : {
            'chosen_covenant' : {},
            'renown_level' : 40 }}}

    Section.covenant(jack, response, None)

    assert jack.covenant == None
    assert jack.renown == 40

def test_covenant_no_renown_level():
    jack = Character('jack')
    response = { 'summary' : {
        'covenant_progress' : {
            'chosen_covenant' : {
                'name' : 'Necrolord' }}}}


    Section.covenant(jack, response, None)

    assert jack.covenant == 'Necrolord'
    assert jack.renown == None

def test_covenant_no_soulbind_section():
    jack = Character('jack')
    response = {
            'summary' : {
                'covenant_progress' : {
                    'chosen_covenant' : {
                        'name' : 'Night Fae' },
                    'renown_level' : 40 }}}

    Section.covenant(jack, response, None)

    assert jack.covenant == 'Night Fae'
    assert jack.renown == 40
    assert jack.current_soulbind == None
