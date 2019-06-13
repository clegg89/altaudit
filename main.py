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
from wowapi import WowApi

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

"""
api = WowApi(tokens['client_id'], tokens['client_secret'])

for character in characters:
    profile = api.get_character_profile(character['region'], character['realm'], character['name'])
"""
