#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Run refresh in a loop
"""
import yaml
import csv
import datetime
import time
import os
import sys
import traceback

from altaudit import Audit

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    audit = Audit(config)
    audit.setup_database()

    while True:
        try:
            result = audit.refresh(datetime.datetime)
            with open('characters.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(result)

            os.system('rsync -razq characters.csv {}'.format(config['server']))
            time.sleep(20)

        except Exception:
            traceback.print_exc(file=sys.stdout)
            continue
