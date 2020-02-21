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
import traceback
import logging

from altaudit import Audit

if __name__ == '__main__':

    logger = logging.getLogger('altaudit')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("altaudit.log")

    logFormat = '[%(levelname)s] [%(asctime)s]: %(message)s'
    dateFormat = '%m-%d-%Y %H:%M:%S'
    formatter = logging.Formatter(logFormat, dateFormat)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.info("Start Program")

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    audit = Audit(config)
    audit.setup_database()
    force_refresh=True

    while True:
        try:
            logger.info("Start Refresh")
            result = audit.refresh(datetime.datetime, force_refresh=force_refresh)
            logger.info("End Refresh")
            with open('characters.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(result)

            logger.info("Upload...")
            os.system('rsync -razq characters.csv {}'.format(config['server']))

            logger.info("Sleep")
            force_refresh=False
            time.sleep(20)

        except:
            logger.exception("Error in refresh")
            continue
