"""Unit Tests for Snapshot models"""
import pytest

from altaudit.models import Character, Snapshot
from altaudit.models.snapshot import Year, Week

def test_create_year_table(db):
    assert db.has_table('years')

def test_create_week_table(db):
    assert db.has_table('weeks')

def test_create_snapshot_table(db):
    assert db.has_table('snapshots')

def test_no_duplicate_years(db_session_integrityerror):
    clegg = Character('clegg')
    y1 = Year(2019, clegg)
    y2 = Year(2019, clegg)

    db_session_integrityerror.add(y1)
    db_session_integrityerror.add(y2)

def test_no_duplicate_weeks(db_session_integrityerror):
    clegg = Character('clegg')
    y = Year(2019, clegg)
    w1 = Week(2, y)
    w2 = Week(2, y)

    db_session_integrityerror.add(w1)
    db_session_integrityerror.add(w2)

def test_no_duplicate_snapshots(db_session_integrityerror):
    clegg = Character('clegg')
    y = Year(2019, clegg)
    w = Week(2, y)
    s1 = Snapshot()
    s2 = Snapshot()
    s1.week = w
    s2.week = w

    db_session_integrityerror.add(s1)
    db_session_integrityerror.add(s2)

def test_add_snapshots_to_character(db_session):
    clegg = Character(name='clegg')
    s1 = Snapshot()
    s1.world_quests = 10
    s1.dungeons = 20
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][3] = s1

    db_session.add(clegg)

    assert s1 == db_session.query(Snapshot)\
                                .join(Week).filter_by(week=3)\
                                .join(Year).filter_by(year=2019)\
                                .join(Character).filter_by(name='clegg').first()

def test_snapshot_default_values(db_session):
    clegg = Character(name='clegg')

    db_session.add(clegg)
    db_session.commit()

    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][3] = Snapshot()

    db_session.flush()
    snapshot = clegg.snapshots[2019][3]

    assert snapshot.world_quests == 0
    assert snapshot.dungeons == 0
    assert snapshot.highest_mplus == 0

