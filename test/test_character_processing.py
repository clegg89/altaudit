"""Unit Tests for the Character data processing"""
import pytest

import datetime

from altaudit.models import Region, Realm, Character, Snapshot
from altaudit.utility import Utility

@pytest.fixture
def mock_section(mocker):
    return mocker.patch('altaudit.models.character.Section')

@pytest.fixture
def mock_update_snapshots(mocker):
    return mocker.patch('altaudit.models.character.Character._update_snapshots')

def test_update_snapshot_add_new_snapshot():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)

    clegg._update_snapshots()

    assert 2019 in clegg.snapshots
    assert 31 in clegg.snapshots[2019]

def test_update_snapshot_no_overwrite_existing():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][31] = Snapshot()
    clegg.snapshots[2019][31].world_quests = 5
    clegg.snapshots[2019][31].dungeons = 10

    Utility.set_refresh_timestamp(now)

    clegg._update_snapshots()

    assert clegg.snapshots[2019][31].world_quests == 5
    assert clegg.snapshots[2019][31].dungeons == 10

def test_update_snapshot_capture_existing_totals():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.world_quests_total = 300
    clegg.dungeons_total = 40

    Utility.set_refresh_timestamp(now)

    clegg._update_snapshots()

    assert clegg.snapshots[2019][31].world_quests == 300
    assert clegg.snapshots[2019][31].dungeons == 40

def test_process_blizzard_last_modified_changed(mock_section, mock_update_snapshots):
    jack = Character('jack', lastmodified=5)
    fake_response = { 'lastModified' : 10 }

    jack.process_blizzard(fake_response, 3, 4, False)

    mock_update_snapshots.assert_called_once()
    mock_section.basic.assert_called_once_with(jack, fake_response, 3)
    mock_section.items.assert_called_once_with(jack, fake_response)
    mock_section.azerite.assert_called_once_with(jack, fake_response, 3, 4)
    mock_section.audit.assert_called_once_with(jack, fake_response, 3, 4)
    mock_section.professions.assert_called_once_with(jack, fake_response)
    mock_section.reputations.assert_called_once_with(jack, fake_response)
    mock_section.pve.assert_called_once_with(jack, fake_response)

def test_process_blizzard_last_modified_not_changed(mock_section, mock_update_snapshots):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'lastModified' : 10 }

    jack.process_blizzard(fake_response, 3, 4, False)

    mock_update_snapshots.assert_called_once()
    mock_section.basic.assert_called_once_with(jack, fake_response, 3)
    mock_section.items.assert_called_once_with(jack, fake_response)
    mock_section.azerite.assert_not_called()
    mock_section.audit.assert_not_called()
    mock_section.professions.assert_called_once_with(jack, fake_response)
    mock_section.reputations.assert_called_once_with(jack, fake_response)
    mock_section.pve.assert_called_once_with(jack, fake_response)

def test_process_blizzard_last_modified_not_changed_force_refresh(mock_section, mock_update_snapshots):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'lastModified' : 10 }

    jack.process_blizzard(fake_response, 3, 4, True)

    mock_update_snapshots.assert_called_once()
    mock_section.basic.assert_called_once_with(jack, fake_response, 3)
    mock_section.items.assert_called_once_with(jack, fake_response)
    mock_section.azerite.assert_called_once_with(jack, fake_response, 3, 4)
    mock_section.audit.assert_called_once_with(jack, fake_response, 3, 4)
    mock_section.professions.assert_called_once_with(jack, fake_response)
    mock_section.reputations.assert_called_once_with(jack, fake_response)
    mock_section.pve.assert_called_once_with(jack, fake_response)

def test_process_raiderio(mock_section):
    jack = Character('jack')

    jack.process_raiderio(4)

    mock_section.raiderio.assert_called_once_with(jack, 4)
