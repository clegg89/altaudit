"""Unit Tests for the Character data processing"""
import pytest

import datetime

from altaudit.models import Region, Realm, Character, Snapshot
from altaudit.utility import Utility

def test_add_new_snapshot():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)

    clegg.update_snapshot()

    assert 2019 in clegg.snapshots
    assert 31 in clegg.snapshots[2019]

def test_no_overwrite_existing():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][31] = Snapshot()
    clegg.snapshots[2019][31].world_quests = 5
    clegg.snapshots[2019][31].dungeons = 10
    clegg.snapshots[2019][31].azerite_power = 30

    Utility.set_refresh_timestamp(now)

    clegg.update_snapshot()

    assert clegg.snapshots[2019][31].world_quests == 5
    assert clegg.snapshots[2019][31].dungeons == 10
    assert clegg.snapshots[2019][31].azerite_power == 30
