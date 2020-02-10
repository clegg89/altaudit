"""Unit Tests for the Character data processing"""
import pytest

import datetime

import altaudit
from altaudit.processing import _update_snapshots, _serialize_azerite, _serialize_gems, _get_snapshots, process_blizzard, process_raiderio, serialize
from altaudit.models import Region, Realm, Character, Snapshot, AzeriteTrait, Gem, GemSlotAssociation
from altaudit.utility import Utility

@pytest.fixture
def mock_section(mocker):
    mock = mocker.MagicMock()
    mocker.patch.object(altaudit.processing, 'sections', [mock])
    return mock

@pytest.fixture
def mock_raiderio(mocker):
    return mocker.patch('altaudit.processing.raiderio')

@pytest.fixture
def mock_update_snapshots(mocker):
    return mocker.patch('altaudit.processing._update_snapshots')

def test_update_snapshot_add_new_snapshot():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)

    _update_snapshots(clegg)

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

    _update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 5
    assert clegg.snapshots[2019][31].dungeons == 10

def test_update_snapshot_capture_existing_totals():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.world_quests_total = 300
    clegg.dungeons_total = 40

    Utility.set_refresh_timestamp(now)

    _update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 300
    assert clegg.snapshots[2019][31].dungeons == 40

def test_process_blizzard_last_modified_changed(mock_section, mock_update_snapshots, mocker):
    jack = Character('jack', lastmodified=5)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10,
        'media' : 'test',
        'equipment' : 'test' } }
    mock_api = mocker.MagicMock()

    process_blizzard(jack, fake_response, None, mock_api, False)

    mock_update_snapshots.assert_called_once()
    mock_section.assert_called_once_with(jack, fake_response, None, mock_api)

def test_process_blizzard_last_modified_not_changed(mock_section, mock_update_snapshots, mocker):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10,
        'media' : 'test',
        'equipment' : 'test' } }
    mock_api = mocker.MagicMock()

    process_blizzard(jack, fake_response, None, mock_api, False)

    mock_update_snapshots.assert_called_once()
    mock_api.get_data_resource.assert_not_called()
    mock_section.assert_not_called()

def test_process_blizzard_last_modified_not_changed_force_refresh(mock_section, mock_update_snapshots, mocker):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10,
        'media' : 'test',
        'equipment' : 'test' } }
    mock_api = mocker.MagicMock()

    process_blizzard(jack, fake_response, None, mock_api, True)

    mock_update_snapshots.assert_called_once()
    mock_section.assert_called_once_with(jack, fake_response, None, mock_api)

@pytest.mark.skip(reason='Move this to sections test')
def test_process_blizzard_basic_before_azerite(mock_section, mock_update_snapshots, mocker):
    jack = Character('jack', lastmodified=5)
    fake_response = { 'lastModified' : 10 }
    manager = mocker.Mock()
    manager.attach_mock(mock_section.basic, 'basic')
    manager.attach_mock(mock_section.azerite, 'azerite')

    process_blizzard(jack, fake_response, 3, 4, False)

    mock_update_snapshots.assert_called_once()
    manager.assert_has_calls([
        mocker.call.basic(jack, fake_response, 3),
        mocker.call.azerite(jack, fake_response, 3, 4)])

@pytest.mark.skip(reason='Move this to sections test')
def test_process_blizzard_basic_before_audit(mock_section, mock_update_snapshots, mocker):
    jack = Character('jack', lastmodified=5)
    fake_response = { 'lastModified' : 10 }
    manager = mocker.Mock()
    manager.attach_mock(mock_section.basic, 'basic')
    manager.attach_mock(mock_section.audit, 'audit')

    process_blizzard(jack, fake_response, 3, 4, False)

    mock_update_snapshots.assert_called_once()
    manager.assert_has_calls([
        mocker.call.basic(jack, fake_response, 3),
        mocker.call.audit(jack, fake_response, 3, 4)])

def test_process_raiderio(mock_raiderio, mocker):
    jack = Character('jack')
    mock_response = mocker.MagicMock()

    process_raiderio(jack, mock_response)

    mock_raiderio.assert_called_once_with(jack, mock_response.json.return_value)

def test_process_raiderio_bad_response(mock_raiderio, mocker):
    jack = Character('jack')
    mock_response = mocker.MagicMock()

    mock_response.ok = False

    process_raiderio(jack, mock_response)

    mock_raiderio.assert_not_called()
    assert jack.raiderio_score == 0
    assert jack.mplus_weekly_highest == 0
    assert jack.mplus_season_highest == 0

def test_serialize_azerite():
    jack = Character('jack')
    jack._head_tier0_selected = AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard')
    jack._head_tier0_available = [
            AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard'),
            AzeriteTrait(12, 234444, 'Made Up Trait', 'inv_fakeicon')]

    _serialize_azerite(jack)

    assert jack.head_tier0_selected == '13+263978+Azerite Empowered+inv_smallazeriteshard'
    assert jack.head_tier0_available == '13+263978+Azerite Empowered+inv_smallazeriteshard|12+234444+Made Up Trait+inv_fakeicon'

def test_serialize_azerite_no_selected():
    jack = Character('jack')
    jack._head_tier0_selected = None
    jack._head_tier0_available = [
            AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard'),
            AzeriteTrait(12, 234444, 'Made Up Trait', 'inv_fakeicon')]

    _serialize_azerite(jack)

    assert jack.head_tier0_selected == None
    assert jack.head_tier0_available == '13+263978+Azerite Empowered+inv_smallazeriteshard|12+234444+Made Up Trait+inv_fakeicon'

def test_serialize_gems():
    jack = Character('jack')
    jack.gems = [
        GemSlotAssociation('wrist',
            Gem(168641, 5, 'Quick Sand Spinel', 'inv_misc_gem_x4_uncommon_perfectcut_yellow', '+50 Haste')),
        GemSlotAssociation('waist',
            Gem(168645, 5, 'Masterful Name', 'inv_misc_gem_x5_uncommon_perfectcut_purple', '+50 Mastery'))
        ]

    _serialize_gems(jack)

    assert jack.gem_ids == '168641|168645'
    assert jack.gem_qualities == '5|5'
    assert jack.gem_names == 'Quick Sand Spinel|Masterful Name'
    assert jack.gem_icons == 'inv_misc_gem_x4_uncommon_perfectcut_yellow|inv_misc_gem_x5_uncommon_perfectcut_purple'
    assert jack.gem_stats == '+50 Haste|+50 Mastery'
    assert jack.gem_slots == 'wrist|waist'

def test_get_snapshots():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : { 32 : Snapshot() } }
    jack.snapshots[2019][32].world_quests = 300
    jack.snapshots[2019][32].dungeons = 20
    jack.world_quests_total = 320
    jack.dungeons_total = 24
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == 20
    assert jack.dungeons_weekly == 4

def test_get_snapshots_negative_world_quests():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : { 32 : Snapshot() } }
    jack.snapshots[2019][32].world_quests = 300
    jack.snapshots[2019][32].dungeons = 20
    jack.world_quests_total = 280
    jack.dungeons_total = 24
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == 0
    assert jack.snapshots[2019][32].world_quests == 280

def test_get_snapshots_negative_dungeons():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : { 32 : Snapshot() } }
    jack.snapshots[2019][32].world_quests = 300
    jack.snapshots[2019][32].dungeons = 20
    jack.world_quests_total = 320
    jack.dungeons_total = 18
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.dungeons_weekly == 0
    assert jack.snapshots[2019][32].dungeons == 18

def test_serialzie(mocker):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    mock_serialize_azerite = mocker.patch('altaudit.processing._serialize_azerite')
    mock_serialize_gems = mocker.patch('altaudit.processing._serialize_gems')
    mock_get_snapshots = mocker.patch('altaudit.processing._get_snapshots')

    altaudit.processing.HEADERS = [ 'name', 'region_name', 'realm_slug' ]

    result = serialize(jack)

    assert result == ['jack', 'us', 'kiljaeden']
    mock_serialize_azerite.assert_called_once()
    mock_serialize_gems.assert_called_once()
    mock_get_snapshots.assert_called_once()
