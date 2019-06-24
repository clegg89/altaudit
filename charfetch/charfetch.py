#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Top-Level functions for the module
"""
from wowapi import WowApi

from .utility import load_or_fetch, load_yaml_file #, convert_to_char_list

def _get_all_character_info(character, now, blizzard_api):
    pass
    # classes = load_or_fetch('classes.pkl', make_fetcher(get_classes, blizzard_api), now)
    # races = load_or_fetch('races.pkl', make_fetcher(get_races, blizzard_api), now)
    # profile = get_char_data(character, blizzard_api)

    # return flatten([get_basic_info(profile, classes, races, character['region']),
    #                 get_all_items(profile['items'])])

def fetch_all(tokens_file, character_file):
    tokens = load_yaml_file(tokens_file)
    WowApi(tokens['blizzard']['client_id'], tokens['blizzard']['client_secret'])

    # characters = convert_to_char_list(load_yaml_file(character_file))

    # for character in characters:
    #     _get_all_character_info(character, now, api)