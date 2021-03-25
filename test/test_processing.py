"""Unit Tests for the Character data processing"""
import pytest

import datetime

from wowapi import WowApiException

import altaudit
from altaudit.processing import update_snapshots, _get_subsections, _serialize_gems, _fill_missing_snapshots,  _get_historical_data, _get_snapshots, process_blizzard, process_raiderio, serialize, PROFILE_API_SECTIONS
from altaudit.models import Region, Realm, Character, Snapshot, Gem, GemSlotAssociation
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
def mock_get_subsections(mocker):
    return mocker.patch('altaudit.processing._get_subsections')

@pytest.fixture
def mock_api(mocker):
    def _get_data_resource(url, region, **filters):
        assert region == 'us'
        assert 'locale' in filters
        assert filters['locale'] == 'en_US'
        if url == 'quests':
            return {'completed' : {'href' : 'completed'}}
        elif url == 'fail':
            raise WowApiException
        return url

    mock = mocker.MagicMock()
    mock.get_data_resource.side_effect = _get_data_resource
    return mock

def test_update_snapshot_add_new_snapshot():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)
    clegg.world_quests_total = 0
    clegg.dungeons_total = 0

    update_snapshots(clegg)

    assert 2019 in clegg.snapshots
    assert 31 in clegg.snapshots[2019]

def test_update_snapshot_do_not_add_on_missing_world_quests():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)
    clegg.dungeons_total = 0

    update_snapshots(clegg)

    assert 2019 in clegg.snapshots
    assert 31 not in clegg.snapshots[2019]

def test_update_snapshot_do_not_add_on_missing_dungeons():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)
    clegg.world_quests_total = 0

    update_snapshots(clegg)

    assert 2019 in clegg.snapshots
    assert 31 not in clegg.snapshots[2019]

def test_update_snapshot_no_overwrite_existing():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.snapshots[2019] = {}
    clegg.snapshots[2019][31] = Snapshot()
    clegg.snapshots[2019][31].world_quests = 5
    clegg.snapshots[2019][31].dungeons = 10
    clegg.snapshots[2019][31].highest_mplus = 13

    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 5
    assert clegg.snapshots[2019][31].dungeons == 10
    assert clegg.snapshots[2019][31].highest_mplus == 13

def test_update_snapshot_capture_existing_totals():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.world_quests_total = 300
    clegg.dungeons_total = 40
    clegg.mplus_weekly_highest = 13
    clegg.snapshots[2019] = { 30 : Snapshot() }

    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 300
    assert clegg.snapshots[2019][31].dungeons == 40
    assert clegg.snapshots[2019][31].highest_mplus == None
    assert clegg.snapshots[2019][30].highest_mplus == 13

def test_update_snapshot_fill_missing_on_new_week(mocker):
    mock_fill_missing_snapshots = mocker.patch('altaudit.processing._fill_missing_snapshots')
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.snapshots[2019] = { 30 : Snapshot() }
    clegg.world_quests_total = 0
    clegg.dungeons_total = 0

    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

    mock_fill_missing_snapshots.assert_called_once_with(clegg)

def test_update_snapshot_fill_missing_not_on_existing_week(mocker):
    mock_fill_missing_snapshots = mocker.patch('altaudit.processing._fill_missing_snapshots')
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.snapshots[2019] = { 31 : Snapshot() }

    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

    mock_fill_missing_snapshots.assert_not_called()

def test_get_subsections_list_of_strings(mock_api, mocker):
    api_sections = ['media', 'equipment', 'reputations']
    profile = { 'summary' : {
        **{v : {'href' : v} for v in api_sections} } }
    expected_api_calls = [mocker.call.get_data_resource(v, 'us', locale='en_US')
            for v in api_sections]

    _get_subsections('us', profile, mock_api, api_sections)

    mock_api.get_data_resource.assert_called()
    assert all([expected == actual for expected, actual in zip(expected_api_calls, mock_api.method_calls)]), "Expected {} got {}".format(expected_api_calls, mock_api.method_calls)
    assert profile['media'] == 'media'
    assert profile['equipment'] == 'equipment'
    assert profile['reputations'] == 'reputations'

def test_get_subsections_list_of_strings_and_dictionaries(mock_api, mocker):
    api_sections = ['media', 'equipment', 'reputations', {'quests' : 'completed'}]
    profile = { 'summary' : {
        'media' : {'href' : 'media'},
        'equipment' : {'href' : 'equipment'},
        'reputations' : {'href' : 'reputations'},
        'quests' : {'href' : 'quests'}}}
    expected_api_calls = [
            mocker.call.get_data_resource('media', 'us', locale='en_US'),
            mocker.call.get_data_resource('equipment', 'us', locale='en_US'),
            mocker.call.get_data_resource('reputations', 'us', locale='en_US'),
            mocker.call.get_data_resource('quests', 'us', locale='en_US'),
            mocker.call.get_data_resource('completed', 'us', locale='en_US')]

    _get_subsections('us', profile, mock_api, api_sections)

    mock_api.get_data_resource.assert_called()
    assert all([expected == actual for expected, actual in zip(expected_api_calls, mock_api.method_calls)]), "Expected {} got {}".format(expected_api_calls, mock_api.method_calls)
    assert profile['media'] == 'media'
    assert profile['equipment'] == 'equipment'
    assert profile['reputations'] == 'reputations'
    assert profile['quests'] == {'completed' : {'href' : 'completed'}}
    assert profile['quests_completed'] == 'completed'

def test_get_subsections_section_missing_from_response(mock_api, mocker):
    api_sections = ['media', 'equipment', 'reputations', {'achievements' : 'statistics'}, {'quests' : 'completed'}]
    profile = { 'summary' : {
        'media' : {'href' : 'media'},
        'equipment' : {'href' : 'equipment'},
        'reputations' : {'href' : 'reputations'},
        'achievements' : {'href' : 'achievements'},
        'quests' : {'href' : 'quests'}}}
    expected_api_calls = [
            mocker.call.get_data_resource('media', 'us', locale='en_US'),
            mocker.call.get_data_resource('equipment', 'us', locale='en_US'),
            mocker.call.get_data_resource('reputations', 'us', locale='en_US'),
            mocker.call.get_data_resource('achievements', 'us', locale='en_US'),
            mocker.call.get_data_resource('quests', 'us', locale='en_US'),
            mocker.call.get_data_resource('completed', 'us', locale='en_US')]

    _get_subsections('us', profile, mock_api, api_sections)

    mock_api.get_data_resource.assert_called()
    assert all([expected == actual for expected, actual in zip(expected_api_calls, mock_api.method_calls)]), "Expected {} got {}".format(expected_api_calls, mock_api.method_calls)
    assert profile['media'] == 'media'
    assert profile['equipment'] == 'equipment'
    assert profile['reputations'] == 'reputations'
    assert profile['quests'] == {'completed' : {'href' : 'completed'}}
    assert profile['quests_completed'] == 'completed'
    assert profile['achievements'] == 'achievements'
    assert profile['achievements_statistics'] == None

def test_get_subsections_handle_wowapi_error(mock_api, mocker):
    api_sections = ['media', 'equipment', {'fail' : 'missing'}, 'reputations']
    profile = { 'summary' : {
        'media' : {'href' : 'media'},
        'equipment' : {'href' : 'equipment'},
        'reputations' : {'href' : 'reputations'},
        'fail' : {'href' : 'fail'}}}

    _get_subsections('us', profile, mock_api, api_sections)

    mock_api.get_data_resource.assert_called()
    assert profile['media'] == 'media'
    assert profile['equipment'] == 'equipment'
    assert profile['reputations'] == 'reputations'
    assert profile['fail'] == None
    assert profile['fail_missing'] == None

def test_process_blizzard_last_modified_not_changed(mock_section, mock_get_subsections):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10}}

    process_blizzard(jack, fake_response, None, None, False)

    mock_section.assert_not_called()
    mock_get_subsections.assert_not_called()

def test_process_blizzard_last_modified_not_changed_force_refresh(mock_section, mock_get_subsections):
    jack = Character('jack', lastmodified=10)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10}}

    process_blizzard(jack, fake_response, None, None, True)

    mock_section.assert_called_once_with(jack, fake_response, None)
    mock_get_subsections.assert_called_once_with(None, fake_response, None, PROFILE_API_SECTIONS)

def test_process_blizzard_always_raise_exception(mock_section, mock_get_subsections):
    jack = Character('jack', lastmodified=5)
    fake_response = { 'summary' : {
        'last_login_timestamp' : 10}}
    mock_get_subsections.side_effect = KeyError()

    with pytest.raises(KeyError):
        process_blizzard(jack, fake_response, None, None, False)

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

def test_get_snapshots_week_not_present():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : {} }
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == None
    assert jack.dungeons_weekly == None

def test_get_snapshots_week_not_present():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : {} }
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == None
    assert jack.dungeons_weekly == None

def test_get_snapshots_year_not_present():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = {}
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == None
    assert jack.dungeons_weekly == None

def test_get_snapshots_snapshot_invalid_leave_as_none():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots = { 2019 : { 32 : Snapshot() } }
    # Values that should not be None are None. totals, snapshot values, etc.
    now = datetime.datetime(2019, 8, 7)
    Utility.set_refresh_timestamp(now)

    _get_snapshots(jack)

    assert jack.world_quests_weekly == None
    assert jack.dungeons_weekly == None

def test_get_historical_data():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots[2019] = {}
    jack.snapshots[2019][52] = Snapshot()
    jack.snapshots[2019][50] = Snapshot()
    jack.snapshots[2019][51] = Snapshot()
    jack.snapshots[2018] = {}
    jack.snapshots[2018][52] = Snapshot()
    jack.snapshots[2020] = {}
    jack.snapshots[2020][2] = Snapshot()
    jack.snapshots[2020][1] = Snapshot()

    jack.snapshots[2018][52].world_quests = 20
    jack.snapshots[2019][50].world_quests = 25
    jack.snapshots[2019][51].world_quests = 40
    jack.snapshots[2019][52].world_quests = 50
    jack.snapshots[2020][1].world_quests = 75
    jack.snapshots[2020][2].world_quests = 100

    jack.snapshots[2018][52].dungeons = 100
    jack.snapshots[2019][50].dungeons = 110
    jack.snapshots[2019][51].dungeons = 120
    jack.snapshots[2019][52].dungeons = 130
    jack.snapshots[2020][1].dungeons = 140
    jack.snapshots[2020][2].dungeons = 170

    jack.snapshots[2018][52].highest_mplus = 8
    jack.snapshots[2019][50].highest_mplus = 12
    jack.snapshots[2019][51].highest_mplus = 3
    # jack.snapshots[2019][52].highest_mplus = None
    jack.snapshots[2020][1].highest_mplus = 13
    # jack.snapshots[2020][2].highest_mplus = None

    _get_historical_data(jack)

    assert jack.historic_world_quests_done == "25|25|10|15|5"
    assert jack.historic_dungeons_done == "30|10|10|10|10"
    assert jack.historic_mplus_done == "13|0|3|12|8"

def test_fill_missing_snapshots():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    jack.snapshots[2017] = {}
    jack.snapshots[2017][52] = Snapshot()
    jack.snapshots[2019] = {}
    jack.snapshots[2019][1] = Snapshot()
    jack.snapshots[2019][3] = Snapshot()

    jack.snapshots[2017][52].world_quests = 10
    jack.snapshots[2019][1].world_quests = 100
    jack.snapshots[2019][3].world_quests = 110

    jack.snapshots[2017][52].dungeons = 5
    jack.snapshots[2019][1].dungeons = 45
    jack.snapshots[2019][3].dungeons = 50

    jack.snapshots[2017][52].highest_mplus = 3
    # jack.snapshots[2019][1].highest_mplus = None
    jack.snapshots[2019][3].highest_mplus = 10

    _fill_missing_snapshots(jack)

    assert 2018 in jack.snapshots
    assert 52 == len(jack.snapshots[2018])

    for week,snapshot in jack.snapshots[2018].items():
        assert snapshot.world_quests == 10, "World Quests wrong on week {}".format(week)
        assert snapshot.dungeons == 5, "Dungeons wrong on week {}".format(week)
        assert snapshot.highest_mplus == None, "Mplus wrong on week {}".format(week)

    assert jack.snapshots[2019][2].world_quests == 100
    assert jack.snapshots[2019][2].dungeons == 45
    assert jack.snapshots[2019][2].highest_mplus == None

def test_serialzie(mocker):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    mock_serialize_gems = mocker.patch('altaudit.processing._serialize_gems')
    mock_get_snapshots = mocker.patch('altaudit.processing._get_snapshots')
    mock_get_historical_data = mocker.patch('altaudit.processing._get_historical_data')

    altaudit.processing.HEADERS = [ 'name', 'region_name', 'realm_slug' ]

    result = serialize(jack)

    assert result == ['jack', 'us', 'kiljaeden']
    mock_serialize_gems.assert_called_once_with(jack)
    mock_get_snapshots.assert_called_once_with(jack)
    mock_get_historical_data.assert_called_once_with(jack)
