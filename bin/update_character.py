#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Update a character's name and/or realm
"""
import yaml
import sys

import altaudit.update as updater

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    if len(sys.argv) < 6:
        print("usage: {} <region> <realmIn> <nameIn> <realmOut> <nameOut>")
        sys.exit(1)

    region = sys.argv[1]
    charIn = {'realm' : sys.argv[2], 'name' : sys.argv[3]}
    charOut = {'realm' : sys.argv[4], 'name' : sys.argv[5]}

    updater.update(config, region, charIn, charOut)

    with open('config.yaml', 'w') as f:
        yaml.dump(config, f)
