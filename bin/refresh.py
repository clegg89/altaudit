#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Run a single refresh
"""
import yaml
import csv
from datetime import datetime
import os

from altaudit import Audit

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    audit = Audit(config)
    audit.setup_database()

    result = audit.refresh(datetime)
    with open('characters.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)

    os.system('rsync -razq characters.csv {}'.format(config['server']))
