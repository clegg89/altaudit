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

def load_or_fetch(stream, fetcher, now):
    stored = pickle.load(stream)

    if now - stored['timestamp'] >= datetime.timedelta(days=1):
        fetch = fetcher()
        fetch['timestamp'] = now
        return fetch

    return stored

"""
def serialize_character(character):
    return [character['region'], character['realm'], character['name']]

with open('characters.yaml', 'r') as f:
    data = yaml.safe_load(f)
with open('tokens.yaml', 'r') as f:
    tokens = yaml.safe_load(f)

characters = [{'name' : character,'realm' : realm,'region' : region} for region,realms in data.items() for realm,characters in realms.items() for character in characters]

print(characters)
print([serialize_character(c) for c in characters])

with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([serialize_character(c) for c in characters])

api = WowApi(tokens['client_id'], tokens['client_secret'])

for character in characters:
    profile = api.get_character_profile(character['region'], character['realm'], character['name'])
"""

def test(**kwargs):
    print(kwargs)

if __name__ == "__main__":
    print(load_yaml_file('characters.yaml'))
    test(locale='en_GB', fields='challenge')
