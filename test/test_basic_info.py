#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Test the Character class
"""
import pytest

import datetime

from charfetch import get_basic_info

@pytest.fixture(scope="module")
def classes():
    return  {
            1 : 'Warrior',
            2 : 'Paladin',
            3 : 'Hunter',
            4 : 'Rogue',
            5 : 'Priest',
            6 : 'Death Knight',
            7 : 'Shaman',
            8 : 'Mage',
            9 : 'Warlock',
            10 : 'Monk',
            11 : 'Druid',
            12 : 'Demon Hunter'}

@pytest.fixture(scope="module")
def races():
    return {
            1 : {'side': 'alliance', 'name': 'Human'},
            2 : {'side': 'horde', 'name': 'Orc'},
            3 : {'side': 'alliance', 'name': 'Dwarf'},
            4 : {'side': 'alliance', 'name': 'Night Elf'},
            5 : {'side': 'horde', 'name': 'Undead'},
            6 : {'side': 'horde', 'name': 'Tauren'},
            7 : {'side': 'alliance', 'name': 'Gnome'},
            8 : {'side': 'horde', 'name': 'Troll'},
            9 : {'side': 'horde', 'name': 'Goblin'},
            10 : {'side': 'horde', 'name': 'Blood Elf'},
            11 : {'side': 'alliance', 'name': 'Draenei'},
            22 : {'side': 'alliance', 'name': 'Worgen'},
            24 : {'side': 'neutral', 'name': 'Pandaren'},
            25 : {'side': 'alliance', 'name': 'Pandaren'},
            26 : {'side': 'horde', 'name': 'Pandaren'},
            27 : {'side': 'horde', 'name': 'Nightborne'},
            28 : {'side': 'horde', 'name': 'Highmountain Tauren'},
            29 : {'side': 'alliance', 'name': 'Void Elf'},
            30 : {'side': 'alliance', 'name': 'Lightforged Draenei'},
            31 : {'side': 'horde', 'name': 'Zandalari Troll'},
            32 : {'side': 'alliance', 'name': 'Kul Tiran'},
            34 : {'side': 'alliance', 'name': 'Dark Iron Dwarf'},
            36 : {'side': 'horde', 'name': "Mag'har Orc"}}

@pytest.fixture
def fake_profile_maker(classes, races):
    def _maker(name='toon1', realm='realm1',
            timestamp=int(datetime.datetime.now().timestamp())*1000,
            kls=9, race=34, gender=0, level=120, mainspec='Destruction',
            media_url='184987488'):
        assert kls in classes
        assert race in races
        assert gender in (0,1)

        faction = 0 if races[race]['side'] == 'alliance' else 1 if races[race]['side'] == 'horde' else 2

        return { 'data' : {
                'community_profile' : {
                    'lastModified' : timestamp,
                    'name' : name,
                    'realm' : realm,
                    'class' : kls,
                    'race' : race,
                    'faction' : faction,
                    'gender' : gender,
                    'level' : level,
                    'thumbnail' : '{0}/96/{1}-avatar.jpg'.format(realm, media_url),
                    'talents' : [
                        { 'selected' : True, 'spec' : { 'name' : mainspec } },
                        { 'selected' : False, 'spec' : { 'name' : 'Failed' } },
                        { 'selected' : False, 'spec' : { 'name' : 'Failed' } }]}},
            'results' : {
                'name' : name,
                'realm' : realm,
                'lastModified' : timestamp,
                'class' : classes[kls],
                'race' : races[race]['name'],
                'faction' : races[race]['side'].capitalize(),
                'gender' : 'Male' if gender == 0 else 'Female',
                'level' : level,
                'thumbnail' : realm + '/96/184987488-avatar.jpg',
                'mainspec' : mainspec,
                'avatar_url' : '{0}/96/{1}-avatar.jpg'.format(realm, media_url),
                'bust_url' : '{0}/96/{1}-inset.jpg'.format(realm, media_url),
                'render_url' : '{0}/96/{1}-main.jpg'.format(realm, media_url)}}

    return _maker

def test_basic_info_name(fake_profile_maker, classes, races):
    profile = fake_profile_maker(name='tony')
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[0] == 'tony'

def test_basic_info_realm(fake_profile_maker, classes, races):
    profile = fake_profile_maker(realm="Zin'azshara")
    result = get_basic_info(profile['data']['community_profile'], classes, races, 'testslug')
    assert result[1] == "Zin'azshara|testslug"

def test_basic_info_region(fake_profile_maker, classes, races):
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races, region='us')
    assert result[2] == 'us'

def test_basic_info_timestamp(fake_profile_maker, classes, races):
    now = datetime.datetime.now().timestamp()*1000
    profile = fake_profile_maker(timestamp=now)
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[3] == now

def test_basic_info_class(fake_profile_maker, classes, races):
    kls = 10
    profile = fake_profile_maker(kls=kls)
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[4] == profile['results']['class']

def test_basic_info_level(fake_profile_maker, classes, races):
    profile = fake_profile_maker(level=45)
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[5] == 45

def test_basic_info_mainspec(fake_profile_maker, classes, races):
    profile = fake_profile_maker(mainspec='Shadow')
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[6] == 'Shadow'

def test_basic_info_faction(fake_profile_maker, classes, races):
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[7] == 'Alliance'

def test_basic_info_gender(fake_profile_maker, classes, races):
    profile = fake_profile_maker(gender=1)
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[8] == 'Female'

def test_basic_info_race(fake_profile_maker, classes, races):
    race = 32
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[9] == profile['results']['race']

def test_basic_info_avatar(fake_profile_maker, classes, races):
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[10] == profile['results']['avatar_url']

def test_basic_info_bust(fake_profile_maker, classes, races):
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[11] == profile['results']['bust_url']

def test_basic_info_render(fake_profile_maker, classes, races):
    profile = fake_profile_maker()
    result = get_basic_info(profile['data']['community_profile'], classes, races)
    assert result[12] == profile['results']['render_url']
