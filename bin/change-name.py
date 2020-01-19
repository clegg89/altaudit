#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Change the name of an existing character and update the database
"""
import yaml
import sys
# import csv
# from datetime import datetime
# import os

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    region = sys.argv[1]
    realm = sys.argv[2]
    characterIn = sys.argv[3]
    characterOut = sys.argv[4]

    index = config['characters'][region][realm].index(characterIn)

    config['characters'][region][realm][index] = characterOut

    with open('out.yaml', 'w') as f:
        yaml.dump(config, f)
