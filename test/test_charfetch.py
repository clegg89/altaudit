#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Unit Tests for main charfetch entry point
"""
import pytest

import datetime

import charfetch

def test_internal_get_metadata(mocker):
    mock_datetime = mocker.MagicMock()
    mock_datetime.utcnow.return_value = "Today's Date and Time"

    result = charfetch.charfetch.get_metadata(mock_datetime)

    mock_datetime.utcnow.assert_called_once()
    assert result[0] == mock_datetime.utcnow.return_value
    assert result[1] == charfetch.charfetch.VERSION

@pytest.fixture
def mock_load_or_fetch(mocker):
    def _mock_load_or_fetch(fileName, fetcher, now, *args, **kwargs):
        if fileName == 'classes.pkl':
            return 'Classes'
        elif fileName == 'races.pkl':
            return 'Races'
        else:
            raise Exception('load_or_fetch called with unrecognized file: {}'.format(fileName))

    fake = mocker.patch('charfetch.charfetch.load_or_fetch')
    fake.side_effect = _mock_load_or_fetch

    return fake

def test_mock_load_or_fetch_classes(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('classes.pkl', 'A', 'B')
    mock_load_or_fetch.assert_called_once_with('classes.pkl', 'A', 'B')
    assert result == 'Classes'

def test_mock_load_or_fetch_races(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('races.pkl', 'A', 'B')
    mock_load_or_fetch.assert_called_once_with('races.pkl', 'A', 'B')
    assert result == 'Races'

def test_mock_load_or_fetch_unknown(mock_load_or_fetch):
    with pytest.raises(Exception):
        result = charfetch.charfetch.mock_load_or_fetch('unknown.pkl', 'C', 'D')

def test_mock_load_or_fetch_args_kwargs(mock_load_or_fetch):
    result = charfetch.charfetch.load_or_fetch('classes.pkl', 'A', 'B', 'test', var1='other')
    mock_load_or_fetch.assert_called_once_with('classes.pkl', 'A', 'B', 'test', var1='other')

@pytest.fixture
def mock_get_char_data(mocker):
    return mocker.patch('charfetch.charfetch.get_char_data')

@pytest.fixture
def mock_get_basic_info(mocker):
    return mocker.patch('charfetch.charfetch.get_basic_info')

@pytest.fixture
def mock_get_all_items(mocker):
    return mocker.patch('charfetch.charfetch.get_all_items')

@pytest.fixture
def mock_get_azerite_info(mocker):
    return mocker.patch('charfetch.charfetch.get_azerite_info')

@pytest.fixture
def mock_get_audit_info(mocker):
    return mocker.patch('charfetch.charfetch.get_audit_info')

@pytest.fixture
def mock_get_profession_info(mocker):
    return mocker.patch('charfetch.charfetch.get_profession_info')

def test_internal_get_all_character_info(mock_load_or_fetch, mock_get_char_data, mock_get_basic_info, mock_get_all_items, mock_get_azerite_info, mock_get_audit_info, mock_get_profession_info, mocker):
    character = {'realm' : 'testrealm', 'region' : 'us'}
    mock_get_char_data.return_value = { 'blizzard' : {
        'community_profile' : { 'items' : 'Items', 'class' : 9, 'professions' : 'Professions' }}}

    mock_get_basic_info.return_value = ['Basic', 'Info']
    mock_get_all_items.return_value = ['All', 'Items']
    mock_get_azerite_info.return_value = [50, 10]
    mock_get_audit_info.return_value = [30, 40]
    mock_get_profession_info.return_value = [20, 15]

    expected_result = ['Basic', 'Info', 'All', 'Items', 50, 10, 30, 40, 20, 15]

    result = charfetch.charfetch._get_all_character_info(character, 'Now', 'Blizzard_API')

    mock_load_or_fetch.assert_has_calls(
            [mocker.call('classes.pkl', charfetch.charfetch.get_classes, 'Now', 'Blizzard_API'),
                mocker.call('races.pkl', charfetch.charfetch.get_races, 'Now', 'Blizzard_API')],
            any_order=True)

    assert result == expected_result

    mock_get_char_data.assert_called_once_with(character, 'Blizzard_API')

    mock_get_basic_info.assert_called_once_with(
            mock_get_char_data.return_value['blizzard']['community_profile'],
            'Classes', 'Races', 'testrealm', 'us')
    mock_get_all_items.assert_called_once_with('Items')
    mock_get_azerite_info.assert_called_once_with('Items', 9, 'Blizzard_API', 'us')
    mock_get_audit_info.assert_called_once_with(mock_get_char_data.return_value['blizzard']['community_profile'], 'Blizzard_API', 'us')
    mock_get_profession_info.assert_called_once_with('Professions')

@pytest.fixture
def fake_tokens():
    return { 'blizzard' : { 'client_id' : 'CLIENT_ID', 'client_secret' : 'CLIENT_SECRET' } }

@pytest.fixture
def fake_server():
    return '192.168.1.1:/var/www/html'

@pytest.fixture
def fake_load_yaml(mocker, fake_tokens, fake_char_yaml, fake_server):
    fake = mocker.patch('charfetch.charfetch.load_yaml_file')
    fake.return_value = {'api' : fake_tokens, 'characters' : fake_char_yaml, 'server' : fake_server }

    return fake

@pytest.fixture
def mock_blizzard_api(mocker):
    return mocker.patch('charfetch.charfetch.WowApi')

def test_mock_blizzard_api(mock_blizzard_api):
    mock_blizzard_api.return_value = 'Test Passed'
    result = charfetch.charfetch.WowApi('TEST_CLIENT_ID', 'TEST_CLIENT_SECRET')
    mock_blizzard_api.assert_called_once_with('TEST_CLIENT_ID', 'TEST_CLIENT_SECRET')
    assert result == 'Test Passed'

@pytest.fixture
def mock_get_all_character_info(mocker):
    return mocker.patch('charfetch.charfetch._get_all_character_info')

class Counter:
    """A sort of generator object that lets us access its current value without incrementing"""
    def __init__(self):
        self.index = 0

    def next(self):
        self.index += 1
        return self.index

def test_charfetch_fetch_all_character_info(mock_blizzard_api, fake_tokens, fake_char_yaml, mock_get_all_character_info, mocker):
    characters = charfetch.utility.convert_to_char_list(fake_char_yaml)
    g = Counter()
    mock_datetime = mocker.MagicMock()
    mock_datetime.now.side_effect = lambda: g.next() # Will keep counting on each call

    def _char_info(character, call_now, api):
        if character not in characters or call_now != g.index or api != mock_blizzard_api.return_value:
            raise Exception("""_get_all_character_info called with unrecognized arguments:
Expected: {}, {}, {}
Actual: {}, {}, {}.""".format(characters, g.index, mock_blizzard_api, character, call_now, api))

        return characters.index(character)

    expected_result = [i for i in range(0,len(characters))]
    mock_get_all_character_info.side_effect = _char_info

    result = charfetch.fetch_all(fake_tokens, fake_char_yaml, mock_datetime)

    assert next(result) == expected_result
    assert next(result) == expected_result

@pytest.fixture
def fake_rows():
    return [[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]]

@pytest.fixture
def mock_fetch_all(mocker, fake_rows):
    mock = mocker.patch('charfetch.charfetch.fetch_all')
    mock.return_value = iter(fake_rows)

    return mock

@pytest.fixture
def mock_csv(mocker):
    return mocker.patch('charfetch.charfetch.csv')

@pytest.fixture
def mock_sleep(mocker):
    return mocker.patch('charfetch.charfetch.time.sleep')

@pytest.fixture
def mock_os(mocker):
    return mocker.patch('charfetch.charfetch.os.system')

@pytest.fixture
def mock_charfetch_open(mocker):
    return mocker.patch('charfetch.charfetch.open', mocker.mock_open())

@pytest.fixture
def mock_get_metadata(mocker):
    mock = mocker.patch('charfetch.charfetch.get_metadata')
    mock.return_value = ['The Date', 'Version']

    return mock

def test_main_load_config_file(mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open):

    charfetch.main()

    fake_load_yaml.assert_called_once_with('config.yaml')

def test_main_fetch_all_called_correctly(mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open):

    charfetch.main()

    mock_fetch_all.assert_called_once()
    args = mock_fetch_all.call_args[0]
    assert fake_load_yaml.return_value['api'] == args[0]
    assert fake_load_yaml.return_value['characters'] == args[1]
    assert datetime.datetime == args[2]

def test_main_get_metadata_called_correctly(mock_get_metadata, mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    charfetch.main()

    mock_get_metadata.assert_has_calls([mocker.call(datetime.datetime), mocker.call(datetime.datetime)])

def test_main_open_called_properly(mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    charfetch.main()

    open_call_args = ['characters.csv', 'w']
    open_call_kwargs = { 'newline' : '' }
    open_call = mocker.call(*open_call_args, **open_call_kwargs)
    assert mock_charfetch_open.call_count == 2
    assert mock_charfetch_open.call_args_list == [open_call, open_call]

def test_main_csv_called_properly(mock_get_metadata, mock_fetch_all, fake_rows, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    charfetch.main()

    writer_call = mocker.call(mock_charfetch_open.return_value)

    metadata_call = mocker.call().writerow((mock_get_metadata.return_value))

    "The call(). format is used for method calls to the object"
    writerows_call = lambda x: mocker.call().writerows(fake_rows[x])

    mock_csv.writer.assert_has_calls([writer_call,
        metadata_call,
        writerows_call(0),
        writer_call,
        metadata_call,
        writerows_call(1)])

def test_main_open_sleep_called_properly(mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    open_call_args = ['characters.csv', 'w']
    open_call_kwargs = { 'newline' : '' }
    manager = mocker.Mock()

    "We use a manager so that we can assure sleep and open were called in correct order"
    manager.attach_mock(mock_charfetch_open, 'open')
    manager.attach_mock(mock_sleep, 'sleep')

    charfetch.main()

    "Obtained the following by just observing what it should come out as"
    manager.assert_has_calls([mocker.call.open(*open_call_args, **open_call_kwargs),
        mocker.call.open().__enter__(),
        mocker.call.open().__exit__(None, None, None),
        mocker.call.sleep(20),
        mocker.call.open(*open_call_args, **open_call_kwargs),
        mocker.call.open().__enter__(),
        mocker.call.open().__exit__(None, None, None),
        mocker.call.sleep(20)])

def test_main_rsync_called(mock_fetch_all, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    charfetch.main()

    mock_os_call = mocker.call('rsync -razq characters.csv ' + fake_load_yaml.return_value['server'])
    mock_os.call_count == 2
    assert mock_os.call_args_list == [mock_os_call, mock_os_call]

def test_main_retry_if_exception(mock_get_metadata, mock_fetch_all, fake_rows, mock_csv, mock_sleep, mock_os,
        fake_load_yaml, mock_charfetch_open, mocker):

    first_call = True
    def _fail_first_call(api, characters, datetime):
        nonlocal first_call
        if first_call:
            first_call = False
            raise Exception('This is a fake exception')
        else:
            return mocker.DEFAULT

    mock_fetch_all.side_effect = _fail_first_call

    charfetch.main()

    writer_call = mocker.call(mock_charfetch_open.return_value)

    metadata_call = mocker.call().writerow(mock_get_metadata.return_value)

    "The call(). format is used for method calls to the object"
    writerows_call = lambda x: mocker.call().writerows(fake_rows[x])

    mock_csv.writer.assert_has_calls([writer_call,
        metadata_call,
        writerows_call(0),
        writer_call,
        metadata_call,
        writerows_call(1)])
