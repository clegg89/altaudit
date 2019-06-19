#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 csmith <csmith@LAPTOP-RUIE9BRU>
#
# Distributed under terms of the MIT license.

"""

"""

import yaml
import csv
import pickle
import datetime
from wowapi import WowApi

def load_yaml_file(fileName):
    """ Convenience function for loading yaml files """
    try:
        with open(fileName, 'r') as f:
            return yaml.safe_load(f)
    except:
        pass

def convert_to_char_list(data):
    """ Convert a dictionary of {region:{realm:[toons]}} to a list of characters """
    try:
        return [{'name' : character, 'realm' : realm, 'region' : region} for region,realms in data.items()
                for realm,characters in realms.items()
                for character in characters]
    except:
        pass

def get_classes(api):
    """ Query api for playabled classes. Return as a dict of form {id:class_name} """
    try:
        return {cl['id']:cl['name'] for cl in api.get_character_classes('us')['classes']}
    except:
        pass

def get_races(api):
    """ Query api for playabled races. Return as a dict of form {id:{'side':side,'name':name}} """
    try:
        return {race['id']:{'side':race['side'],'name':race['name']} for race in api.get_character_races('us')['races']}
    except:
        pass

def get_char_profile(character, api, **filters):
    """ Query api for character's data return it """
    try:
        return api.get_character_profile(character['region'], character['realm'], character['name'], **filters)
    except:
        pass

def _fetch_and_stored(fname, fetcher, now):
    fetch = {}
    fetch['data'] = fetcher()
    fetch['timestamp'] = now
    with open(fname, 'wb') as tf:
        pickle.dump(fetch, tf, pickle.HIGHEST_PROTOCOL)

    return fetch['data']

def load_or_fetch(fname, fetcher, now):
    try :
        with open(fname, 'rb') as tf:
            stored = pickle.load(tf)
    except FileNotFoundError:
        return _fetch_and_stored(fname, fetcher, now)

    if now - stored['timestamp'] >= datetime.timedelta(days=1):
        return _fetch_and_stored(fname, fetcher, now)

    return stored['data']

"""
with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([serialize_character(c) for c in characters])
"""

def get_all_info(character, api, now):
    classes = load_or_fetch('classes.pkl', lambda: get_classes(api), now)
    races = load_or_fetch('races.pkl', lambda: get_races(api), now)

    profile = get_char_profile(character, api)

    character_class = classes[profile['class']]
    race = races[profile['race']]['name']
    faction = 'Alliance' if profile['faction'] is 0 else 'Horde'
    gender = 'Male' if profile['gender'] is 0 else 'Female'
    for spec in profile['talents']:
        if 'selected' in spec and spec['selected']:
            current_spec = spec['spec']['name']

    return [character['name'], character['region'], character['realm'], character_class, profile['level'], current_spec, faction, gender, race]

if __name__ == "__main__":
    tokens = load_yaml_file('tokens.yaml')
    characters = convert_to_char_list(load_yaml_file('characters.yaml'))
    api = WowApi(tokens['client_id'], tokens['client_secret'])
    output = []
    # for character in characters:
    #     output.append(get_all_info(character, api))
