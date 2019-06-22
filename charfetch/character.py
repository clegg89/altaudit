#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Functions to get information about a character
"""
from statistics import mean

def get_basic_info(profile, classes, races, region=''):
    mainspec = None
    for spec in profile['talents']:
        if 'selected' in spec and spec['selected']:
            mainspec = spec['spec']['name']

    return [profile['name'], profile['realm'], region,
            profile['lastModified'], classes[profile['class']],
            profile['level'],
            mainspec,
            'Alliance' if profile['faction'] == 0 else 'Horde' if profile['faction'] == 1 else 'Neutral',
            'Male' if profile['gender'] == 0 else 'Female' if profile['gender'] == 1 else None,
            races[profile['race']]['name']]

def _get_item(item_dictionary):
    return [item_dictionary['itemLevel'],
            item_dictionary['id'],
            item_dictionary['name'],
            item_dictionary['icon'],
            item_dictionary['quality']]

def get_all_items(items_dictionary):
    return [mean([item['itemLevel'] for item in items_dictionary.values()])]
