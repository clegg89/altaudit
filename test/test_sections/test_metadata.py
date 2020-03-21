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
    assert Section.metadata()[3] == "Uldir+Taloc_MOTHER_Fetid Devourer_Zek'voz, Herald of N'zoth_Vectis_Zul, Reborn_Mythrax the Unraveler_G'huun|Battle of Dazar'alor+Champion of the Light_Grong_Jadefire Masters_Opulence_Conclave of the Chosen_King Rastakhan_Mekkatorque_Stormwall Blockade_Lady Jaina Proudmoore|Crucible of Storms+The Restless Cabal_Uu'nat, Harbinger of the Void|The Eternal Palace+Abyssal Commander Sivara_Radiance of Azshara_Blackwater Behemoth_Lady Ashvane_Orgozoa_The Queen's Court_Za'qul_Queen Azshara"
