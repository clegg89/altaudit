"""Unit Tests for the Character data processing"""
import pytest

import datetime

from wowapi import WowApiException

import altaudit
from altaudit.processing import update_snapshots, _get_subsections, _serialize_azerite, _serialize_gems, _get_snapshots, process_blizzard, process_raiderio, serialize, PROFILE_API_SECTIONS
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
def mock_get_subsections(mocker):
    return mocker.patch('altaudit.processing._get_subsections')

@pytest.fixture
def mock_api(mocker):
    def _get_data_resource(url, region):
        assert region == 'us'
        assert url.endswith("&locale=en_US")
        actual_url = url.replace("&locale=en_US","")
        if actual_url == 'quests':
            return {'completed' : {'href' : 'completed'}}
        elif actual_url == 'fail':
            raise WowApiException
        return actual_url

    mock = mocker.MagicMock()
    mock.get_data_resource.side_effect = _get_data_resource
    return mock

def test_update_snapshot_add_new_snapshot():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

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

    update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 5
    assert clegg.snapshots[2019][31].dungeons == 10

def test_update_snapshot_capture_existing_totals():
    clegg = Character('clegg', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 5)
    clegg.world_quests_total = 300
    clegg.dungeons_total = 40

    Utility.set_refresh_timestamp(now)

    update_snapshots(clegg)

    assert clegg.snapshots[2019][31].world_quests == 300
    assert clegg.snapshots[2019][31].dungeons == 40

def test_get_subsections_list_of_strings(mock_api, mocker):
    api_sections = ['media', 'equipment', 'reputations']
    profile = { 'summary' : {
        **{v : {'href' : v} for v in api_sections} } }
    expected_api_calls = [mocker.call.get_data_resource('{}&locale=en_US'.format(v), 'us')
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
            mocker.call.get_data_resource('{}&locale=en_US'.format('media'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('equipment'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('reputations'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('quests'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('completed'), 'us')]

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
            mocker.call.get_data_resource('{}&locale=en_US'.format('media'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('equipment'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('reputations'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('achievements'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('quests'), 'us'),
            mocker.call.get_data_resource('{}&locale=en_US'.format('completed'), 'us')]

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

    mock_section.assert_called_once_with(jack, fake_response, None, None)
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

def test_serialzie(mocker):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    mock_serialize_azerite = mocker.patch('altaudit.processing._serialize_azerite')
    mock_serialize_gems = mocker.patch('altaudit.processing._serialize_gems')
    mock_get_snapshots = mocker.patch('altaudit.processing._get_snapshots')

    altaudit.processing.HEADERS = [ 'name', 'region_name', 'realm_slug' ]

    result = serialize(jack)

    assert result == ['jack', 'us', 'kiljaeden']
    mock_serialize_azerite.assert_called_once_with(jack)
    mock_serialize_gems.assert_called_once_with(jack)
    mock_get_snapshots.assert_called_once_with(jack)
