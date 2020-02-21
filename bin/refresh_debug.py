#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Run a single refresh with debug logging. Do not upload to server
"""
import yaml
import csv
from datetime import datetime
import os
import traceback
import logging

from altaudit import Audit

if __name__ == '__main__':

    logger = logging.getLogger('altaudit')
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("altaudit.log")
    console = logging.StreamHandler()

    logFormat = '[%(levelname)s] [%(asctime)s]: %(message)s'
    dateFormat = '%m-%d-%Y %H:%M:%S'
    formatter = logging.Formatter(logFormat, dateFormat)

    handler.setFormatter(formatter)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

    logger.info("Start Program")

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    audit = Audit(config)
    audit.setup_database()

    try:
        logger.info("Start Refresh")
        result = audit.refresh(datetime, force_refresh=True)
        logger.info("End Refresh")
        with open('characters.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)

        logger.info("Complete")

    except:
        logger.exception("Error in refresh")
