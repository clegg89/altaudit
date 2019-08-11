#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for altaudit.utility
"""
import pytest

import datetime

from altaudit.utility import Utility

def test_utility_region_times_before_reset():
    now = datetime.datetime(2019, 8, 5, 20, 32, 34, 85)

    Utility.set_refresh_timestamp(now)

    assert Utility.year['us'] == 2019
    assert Utility.year['eu'] == 2019
    assert Utility.year['kr'] == 2019
    assert Utility.year['tw'] == 2019

    assert Utility.week['us'] == 31
    assert Utility.week['eu'] == 31
    assert Utility.week['kr'] == 31
    assert Utility.week['tw'] == 31

def test_utility_region_times_between_us_eu():
    now = datetime.datetime(2019, 8, 6, 20, 31, 44, 0)

    Utility.set_refresh_timestamp(now)

    assert Utility.year['us'] == 2019
    assert Utility.year['eu'] == 2019
    assert Utility.year['kr'] == 2019
    assert Utility.year['tw'] == 2019

    assert Utility.week['us'] == 32
    assert Utility.week['eu'] == 31
    assert Utility.week['kr'] == 31
    assert Utility.week['tw'] == 31

def test_utility_region_times_after_us_eu():
    now = datetime.datetime(2019, 8, 8, 20, 31, 44, 0)

    Utility.set_refresh_timestamp(now)

    assert Utility.year['us'] == 2019
    assert Utility.year['eu'] == 2019
    assert Utility.year['kr'] == 2019
    assert Utility.year['tw'] == 2019

    assert Utility.week['us'] == 32
    assert Utility.week['eu'] == 32
    assert Utility.week['kr'] == 32
    assert Utility.week['tw'] == 32

def test_utility_region_times_use_isocalendar():
    now = datetime.datetime(2020, 1, 3, 20, 44)

    Utility.set_refresh_timestamp(now)

    assert Utility.year['us'] == 2020
    assert Utility.year['eu'] == 2020
    assert Utility.year['kr'] == 2020
    assert Utility.year['tw'] == 2020

    assert Utility.week['us'] == 1
    assert Utility.week['eu'] == 1
    assert Utility.week['kr'] == 1
    assert Utility.week['tw'] == 1

def test_utility_region_timestamps():
    now = datetime.datetime(2019, 8, 8, 20, 31, 44, 0)

    Utility.set_refresh_timestamp(now)

    assert Utility.timestamp['us'] == 1565103600
    assert Utility.timestamp['eu'] == 1565161200
    assert Utility.timestamp['kr'] == 1565161200
    assert Utility.timestamp['tw'] == 1565161200

def test_utility_refresh_time():
    now = datetime.datetime(2019, 8, 8, 20, 31, 44, 0)

    Utility.set_refresh_timestamp(now)

    assert Utility.refresh_time == now
