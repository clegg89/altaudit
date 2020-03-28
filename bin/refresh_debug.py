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
import datetime
import os
import logging

from altaudit import Audit

class fake_dt:
    @classmethod
    def utcnow(cls):
        # return datetime.datetime.utcnow()
        return datetime.datetime.utcnow() + datetime.timedelta(7)

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
        result = audit.refresh(fake_dt, force_refresh=True)
        logger.info("End Refresh")
        with open('characters.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)

        logger.info("Complete")

    except:
        logger.exception("Error in refresh")
