#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Utility functions used throughout altaudit
"""
import datetime
import time
import yaml
import pickle

from .constants import WEEKLY_RESETS

class Utility:
    "Convenience class to hold static variables and functions"
    year = {}
    week = {}
    timestamp = {}
    refresh_time = None

    @classmethod
    def set_refresh_timestamp(cls, now):
        """
        Save Timestamp (year and week) at beginning of a new refresh operation.

        This will help prevent odd behavior around reset times

        @note We can still get some odd behavior as some of the API
        requests may occur before the reset and others after the reset.
        This will make some things (like the island weekly) seem off.
        Luckily it should all work out on the next refresh, and working
        trying to work around it is too complicated for the pay off
        """
        # Store the actual refresh timestamp
        cls.refresh_time = now

        # Go back to the last hour mark
        time_now = datetime.datetime.combine(now.date(), datetime.time(now.hour))

        for region,reset in WEEKLY_RESETS.items():
            reset_time = time_now

            # Go back in hours until we get to 15:00 UTC
            while reset_time.hour != reset['hour']:
                reset_time -= datetime.timedelta(hours=1)

            # Go back in days until we get to Tuesday
            while reset_time.weekday() != time.strptime(reset['day'], '%A').tm_wday:
                reset_time -= datetime.timedelta(1)

            cls.year[region] = reset_time.isocalendar()[0]
            cls.week[region] = reset_time.isocalendar()[1]
            cls.timestamp[region] = int((reset_time - datetime.datetime.utcfromtimestamp(0)).total_seconds())
