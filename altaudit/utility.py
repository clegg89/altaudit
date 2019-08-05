#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Utility functions used throughout altaudit
"""
import datetime
import time
import yaml
import pickle

from .constants import WEEKLY_RESETS

class Utility:
    "Convenience class to hold static variables and functions"
    year = {}
    week = {}

    @classmethod
    def set_refresh_timestamp(cls, now):
        """
        Save Timestamp (year and week) at beginning of a new refresh operation.

        This will help prevent odd behavior around reset times

        @note We can still get some odd behavior as some of the API
        requests may occur before the reset and others after the reset.
        This will make some things (like the island weekly) seem off.
        Luckily it should all work out on the next refresh, and working
        trying to work around it is too complicated for the pay off
        """
        # Go back to the last hour mark
        time_now = datetime.datetime.combine(now.date(), datetime.time(now.hour))

        for region,reset in WEEKLY_RESETS.items():
            reset_time = time_now

            # Go back in hours until we get to 15:00 UTC
            while reset_time.hour != reset['hour']:
                reset_time -= datetime.timedelta(hours=1)

            # Go back in days until we get to Tuesday
            while reset_time.weekday() != time.strptime(reset['day'], '%A').tm_wday:
                reset_time -= datetime.timedelta(1)

            cls.year[region] = reset_time.isocalendar()[0]
            cls.week[region] = reset_time.isocalendar()[1]


def flatten(l):
    """ Recursively convert a list of lists to a single flat list """
    output = []

    for i in l:
        if type(i) == list:
            output += flatten(i)
        else:
            output.append(i)

    return output

def load_yaml_file(fileName):
    """ Convenience function for loading yaml files """
    with open(fileName, 'r') as f:
        return yaml.safe_load(f)

def convert_to_char_list(data):
    """ Convert a dictionary of {region:{realm:[toons]}} to a list of characters """
    try:
        return [{'name' : character, 'realm' : realm, 'region' : region} for region,realms in data.items()
                for realm,characters in realms.items()
                for character in characters]
    except:
        pass

def get_classes(api):
    """ Query Blizzard API for playabled classes. Return as a dict of form {id:class_name} """
    raw = api.get_character_classes('us', locale='en_US')
    return {kls['id']:kls['name'] for kls in raw['classes']}

def get_races(api):
    """ Query Blizzard API for playabled races. Return as a dict of form {id:{'side':side,'name':name}} """
    raw = api.get_character_races('us', locale='en_US')
    return {race['id']:{'side':race['side'],'name':race['name']} for race in raw['races']}

def get_char_data(character, blizzard_api):
    """ Query API's for character's data and return it """

    return { 'blizzard' : {
        'community_profile' : blizzard_api.get_character_profile(character['region'],
            character['realm'], character['name'],
            locale='en_US', fields='statistics,talents,reputation,items,achievements,audit,professions')}}

# Left as an example for how to get profile API data
"""
'media' : blizzard_api.get_resource('profile/wow/character/{0}/{1}/character-media', 'us',
    *[character['realm'], character['name']], locale='en_US', namespace='profile-us')}}
"""

def load_or_fetch(fname, fetcher, now, *fetchargs, **fetchkwargs):
    def _fetch_and_store(fname, fetcher, now):
        fetch = {}
        fetch['data'] = fetcher(*fetchargs, **fetchkwargs)
        fetch['timestamp'] = now
        with open(fname, 'wb') as tf:
            pickle.dump(fetch, tf, pickle.HIGHEST_PROTOCOL)

        return fetch['data']

    try :
        with open(fname, 'rb') as tf:
            stored = pickle.load(tf)
    except FileNotFoundError:
        return _fetch_and_store(fname, fetcher, now)

    if now - stored['timestamp'] >= datetime.timedelta(days=1):
        return _fetch_and_store(fname, fetcher, now)

    return stored['data']
