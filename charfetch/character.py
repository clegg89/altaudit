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
    if item_dictionary:
        return [item_dictionary['itemLevel'],
                item_dictionary['id'],
                item_dictionary['name'],
                item_dictionary['icon'],
                item_dictionary['quality']]
    else:
        return [None, None, None, None, None]

def get_all_items(items_dictionary):
    slots = ['head', 'neck', 'shoulder', 'back',
            'chest', 'wrist', 'hands', 'waist',
            'legs', 'feet', 'finger1', 'finger2',
            'trinket1', 'trinket2', 'mainHand', 'offHand']

    ilevels = {}
    items = []
    for slot in slots:
        ilevels[slot] = items_dictionary[slot]['itemLevel'] if slot in items_dictionary else 0
        items.append(_get_item(items_dictionary[slot]) if slot in items_dictionary else _get_item(None))

    # Special case for missing offHand
    # Note: This is not technically correct. Blizzard will only replace
    # the offHand slot if the mainHand slot is a 2h weapon.
    # However, we don't have enough information from the character item
    # list to determine this. We could query the Item API and use the
    # class/subclass to determine if it is 1h/2h, but that's a lot of
    # extra work, for very little reward. We'll mark it as a todo
    # TODO Query wow API to determine if mainHand is 1h or 2h
    if ilevels['offHand'] == 0:
        ilevels['offHand'] = ilevels['mainHand']

    ilvls = list(ilevels.values())

    equipped_ilvl = mean(ilvls)

    for idx,ilvl in enumerate(ilvls):
        if ilvl == 0:
            ilvls[idx] = None

    return [equipped_ilvl] + items
