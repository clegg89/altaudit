"""Unit Tests for Snapshot models"""
import pytest

from sqlalchemy.exc import IntegrityError

from altaudit.models import Character, Snapshot
from altaudit.models.snapshot import Year, Week

def test_add_snapshots_to_character(db_session):
    clegg = Character(name='clegg')
    s1 = Snapshot()
    s1.world_quests = 10
    s1.dungeons = 20
    s1.azerite_power = 1500
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][3] = s1

    db_session.add(clegg)

    assert s1 == db_session.query(Snapshot)\
                                .join(Week).filter_by(week=3)\
                                .join(Year).filter_by(year=2019)\
                                .join(Character).filter_by(name='clegg').first()
