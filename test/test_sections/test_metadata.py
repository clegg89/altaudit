"""Unit Tests for metadata"""
import pytest

import datetime

from altaudit.utility import Utility
from altaudit.version import VERSION, WOW_PATCH

import altaudit.sections as Section

def test_metadata_timestamp():
    now = datetime.datetime(2019, 8, 11, 18, 1, 30)

    Utility.set_refresh_timestamp(now)

    assert Section.metadata()[0] == now

def test_metadata_software_version():
    assert Section.metadata()[1] == VERSION

def test_metadata_wow_patch():
    assert Section.metadata()[2] == WOW_PATCH

def test_metadata_raids():
    assert Section.metadata()[3] == "Castle Nathria+Shriekwing_Huntsman Altimor_Hungering Destroyer_Sun King's Salvation_Artificer Xy'mox_Lady Inerva Darkvein_The Council of Blood_Sludgefist_Stone Legion Generals_Sire Denathrius"
