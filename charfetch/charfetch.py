#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Top-Level functions for the module
"""
from wowapi import WowApi
import csv
import datetime
import time
import os

from .utility import load_or_fetch, load_yaml_file, get_classes, get_races, get_char_data, flatten, convert_to_char_list
from .character import get_basic_info, get_all_items, get_azerite_info, get_audit_info, get_profession_info

VERSION = 820

def _get_all_character_info(character, now, blizzard_api):
    classes = load_or_fetch('classes.pkl', get_classes, now, blizzard_api)
    races = load_or_fetch('races.pkl', get_races, now, blizzard_api)
    profile = get_char_data(character, blizzard_api)['blizzard']
    community_profile = profile['community_profile']

    return flatten([get_basic_info(community_profile, classes, races, character['realm'], character['region']),
                    get_all_items(community_profile['items']),
                    get_azerite_info(community_profile['items'],
                        community_profile['class'], blizzard_api, character['region']),
                    get_audit_info(community_profile, blizzard_api, character['region']),
                    get_profession_info(community_profile['professions'])])

def fetch_all(tokens, characters_yaml, dt):
    api = WowApi(tokens['blizzard']['client_id'], tokens['blizzard']['client_secret'])

    characters = convert_to_char_list(characters_yaml)

    while True:
        rows = []
        for character in characters:
            rows.append(_get_all_character_info(character, dt.now(), api))

        yield rows

def get_metadata(dt):
    return [dt.utcnow(), VERSION]

def _main(config):
    for characters in fetch_all(config['api'], config['characters'], datetime.datetime):
        print("Write rows to csv...")
        metadata = get_metadata(datetime.datetime)
        with open('characters.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(metadata)
            writer.writerows(characters)
        print("Sync")
        os.system('rsync -razq characters.csv {}'.format(config['server']))
        print("Sleep")
        time.sleep(20)
        print("Do next fetch")

def main():
    print("Starting...")
    config = load_yaml_file('config.yaml')
    while True:
        try:
            _main(config)
        except Exception as e:
            print(e)
            continue
        break
