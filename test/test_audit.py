"""Unit Tests for the Audit class"""
import pytest

from unittest.mock import patch

import datetime

from altaudit.audit import Audit, RAIDERIO_URL
from altaudit.utility import Utility
from altaudit.models import Base, Faction, Class, Race, Region, Realm, Character, Gem
from altaudit.blizzard import BLIZZARD_LOCALE
from altaudit.gem_enchant import gem_lookup
import altaudit.sections as Section

wow_classes = {'classes': [
    {'id': 1, 'name': 'Warrior'},
    {'id': 2, 'name': 'Paladin'},
    {'id': 3, 'name': 'Hunter'},
    {'id': 4, 'name': 'Rogue'},
    {'id': 5, 'name': 'Priest'},
    {'id': 6, 'name': 'Death Knight'},
    {'id': 7, 'name': 'Shaman'},
    {'id': 8, 'name': 'Mage'},
    {'id': 9, 'name': 'Warlock'},
    {'id': 10, 'name': 'Monk'},
    {'id': 11, 'name': 'Druid'},
    {'id': 12, 'name': 'Demon Hunter'}]}

wow_races = {'races': [
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/1?namespace=static-8.3.0_32861-us'}, 'name': 'Human', 'id': 1},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/2?namespace=static-8.3.0_32861-us'}, 'name': 'Orc', 'id': 2},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/3?namespace=static-8.3.0_32861-us'}, 'name': 'Dwarf', 'id': 3},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/4?namespace=static-8.3.0_32861-us'}, 'name': 'Night Elf', 'id': 4},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/5?namespace=static-8.3.0_32861-us'}, 'name': 'Undead', 'id': 5},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/6?namespace=static-8.3.0_32861-us'}, 'name': 'Tauren', 'id': 6},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/7?namespace=static-8.3.0_32861-us'}, 'name': 'Gnome', 'id': 7},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/8?namespace=static-8.3.0_32861-us'}, 'name': 'Troll', 'id': 8},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/9?namespace=static-8.3.0_32861-us'}, 'name': 'Goblin', 'id': 9},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/10?namespace=static-8.3.0_32861-us'}, 'name': 'Blood Elf', 'id': 10},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/11?namespace=static-8.3.0_32861-us'}, 'name': 'Draenei', 'id': 11},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/22?namespace=static-8.3.0_32861-us'}, 'name': 'Worgen', 'id': 22},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/24?namespace=static-8.3.0_32861-us'}, 'name': 'Pandaren', 'id': 24},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/25?namespace=static-8.3.0_32861-us'}, 'name': 'Pandaren', 'id': 25},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/26?namespace=static-8.3.0_32861-us'}, 'name': 'Pandaren', 'id': 26},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/27?namespace=static-8.3.0_32861-us'}, 'name': 'Nightborne', 'id': 27},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/28?namespace=static-8.3.0_32861-us'}, 'name': 'Highmountain Tauren', 'id': 28},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/29?namespace=static-8.3.0_32861-us'}, 'name': 'Void Elf', 'id': 29},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/30?namespace=static-8.3.0_32861-us'}, 'name': 'Lightforged Draenei', 'id': 30},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/31?namespace=static-8.3.0_32861-us'}, 'name': 'Zandalari Troll', 'id': 31},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/32?namespace=static-8.3.0_32861-us'}, 'name': 'Kul Tiran', 'id': 32},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/34?namespace=static-8.3.0_32861-us'}, 'name': 'Dark Iron Dwarf', 'id': 34},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/35?namespace=static-8.3.0_32861-us'}, 'name': 'Vulpera', 'id': 35},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/36?namespace=static-8.3.0_32861-us'}, 'name': "Mag'har Orc", 'id': 36},
    {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-race/37?namespace=static-8.3.0_32861-us'}, 'name': 'Mechagnome', 'id': 37}]}

wow_race_details = {
    1 : {'id': 1, 'name': 'Human', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    2 : {'id': 2, 'name': 'Orc', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    3 : {'id': 3, 'name': 'Dwarf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    4 : {'id': 4, 'name': 'Night Elf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    5 : {'id': 5, 'name': 'Undead', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    6 : {'id': 6, 'name': 'Tauren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    7 : {'id': 7, 'name': 'Gnome', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    8 : {'id': 8, 'name': 'Troll', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    9 : {'id': 9, 'name': 'Goblin', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    10 : {'id': 10, 'name': 'Blood Elf', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    11 : {'id': 11, 'name': 'Draenei', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    22 : {'id': 22, 'name': 'Worgen', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    24 : {'id': 24, 'name': 'Pandaren', 'faction': {'type': 'NEUTRAL', 'name': 'Neutral'}, 'is_selectable': True, 'is_allied_race': False},
    25 : {'id': 25, 'name': 'Pandaren', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': False, 'is_allied_race': False},
    26 : {'id': 26, 'name': 'Pandaren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': False, 'is_allied_race': False},
    27 : {'id': 27, 'name': 'Nightborne', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    28 : {'id': 28, 'name': 'Highmountain Tauren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    29 : {'id': 29, 'name': 'Void Elf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    30 : {'id': 30, 'name': 'Lightforged Draenei', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    31 : {'id': 31, 'name': 'Zandalari Troll', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    32 : {'id': 32, 'name': 'Kul Tiran', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    34 : {'id': 34, 'name': 'Dark Iron Dwarf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    35 : {'id': 35, 'name': 'Vulpera', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    36 : {'id': 36, 'name': "Mag'har Orc", 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    37 : {'id': 37, 'name': 'Mechagnome', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True}}

@pytest.fixture
def mock_session_get(mocker):
    return mocker.patch('altaudit.audit.requests.Session.get')

@pytest.fixture
def mock_process_blizzard(mocker):
    return mocker.patch('altaudit.audit.process_blizzard')

@pytest.fixture
def mock_update_snapshots(mocker):
    return mocker.patch('altaudit.audit.update_snapshots')

@pytest.fixture
def mock_process_raiderio(mocker):
    return mocker.patch('altaudit.audit.process_raiderio')

@pytest.fixture
def mock_serialize(mocker):
    mock = mocker.patch('altaudit.audit.serialize')
    mock.return_value = [1, 2, 3, 4]

    return mock

@pytest.fixture
def mock_writer(mocker):
    return mocker.MagicMock()

class TestAuditInit:
    @classmethod
    def setup_class(cls):
        cls.config = {
                'api' : {
                    'blizzard' : {
                        'client_id' : 'MY_CLIENT_ID',
                        'client_secret' : 'MY_CLIENT_SECRET' },
                    'wcl' : { 'public_key' : 'MY_WCL_KEY' }},
                'characters' : {
                    'us' : {
                        'kiljaeden' : [
                            'clegg', 'salvorhardin'],
                        'lightbringer' : [
                            'clegg']},
                    'eu' : {
                        'kiljaeden' : [
                            'clegg']}},
                'database' : 'sqlite://'}

    def setup_method(self, method):
        with patch('altaudit.audit.WowApi') as MockApiClass:
            def _get_data_resource(url, region):
                assert region == 'us'
                for r in wow_races['races']:
                    if url == "{}&{}".format(r['key']['href'], 'locale=en_US'):
                        return wow_race_details[r['id']]

                assert False, "Race url not found: {}".format(url)

            def _get_playable_race(region, namespace, race_id, locale=None):
                assert region == 'us'
                assert namespace == 'static-us'
                assert locale == 'en_US'
                return wow_race_details[race_id]

            self.mock_wowapi = MockApiClass
            mock_api = MockApiClass.return_value
            mock_api.get_playable_class_index.return_value = wow_classes
            mock_api.get_playable_race_index.return_value = wow_races
            mock_api.get_playable_race.side_effect = _get_playable_race
            mock_api.get_data_resource.side_effect = _get_data_resource

            self.mock_blizzard_api = mock_api

            self.audit = Audit(self.config)
            Base.metadata.create_all(self.audit.engine)

    @pytest.fixture
    def db_session(self):
        session = self.audit.make_session()
        yield session
        session.close()

    def test_engine_created(self):
        assert self.audit.engine.name == 'sqlite'

    def test_blizzard_api_created(self):
        self.mock_wowapi.assert_called_once_with(client_id='MY_CLIENT_ID',
                client_secret='MY_CLIENT_SECRET',
                retry_conn_failures=True)

    def test_has_tables(self):
        assert self.audit.engine.has_table('classes')
        assert self.audit.engine.has_table('factions')
        assert self.audit.engine.has_table('races')
        assert self.audit.engine.has_table('regions')
        assert self.audit.engine.has_table('realms')
        assert self.audit.engine.has_table('characters')
        assert self.audit.engine.has_table('years')
        assert self.audit.engine.has_table('weeks')
        assert self.audit.engine.has_table('snapshots')

    def test_classes_retrieved(self, db_session):
        self.audit._create_classes(db_session)

        query = db_session.query(Class)
        classes = {c.id : c.name for c in query.all()}

        assert query.count() == 12
        assert classes[1] == 'Warrior'
        assert classes[2] == 'Paladin'
        assert classes[3] == 'Hunter'
        assert classes[4] == 'Rogue'
        assert classes[5] == 'Priest'
        assert classes[6] == 'Death Knight'
        assert classes[7] == 'Shaman'
        assert classes[8] == 'Mage'
        assert classes[9] == 'Warlock'
        assert classes[10] == 'Monk'
        assert classes[11] == 'Druid'
        assert classes[12] == 'Demon Hunter'

    def test_old_classes_deleted(self, db_session):
        self.audit._create_classes(db_session)

        db_session.add(Class('Tinkerer', id=14))
        db_session.commit()

        self.audit._create_classes(db_session)

        assert db_session.query(Class).count() == 12
        assert db_session.query(Class).filter_by(name='Tinkerer').first() == None

    def test_races_factions_created(self, db_session):
        self.audit._create_races(db_session)

        query = db_session.query(Faction)
        factions = {f.id : f.name for f in query.all()}

        assert query.count() == 3
        assert query.filter_by(name='Alliance').first() != None
        assert query.filter_by(name='Horde').first() != None
        assert query.filter_by(name='Neutral').first() != None

    def test_races_factions_recreated(self, db_session):
        self.audit._create_races(db_session)

        db_session.add(Faction('junk', id=4))
        db_session.commit()

        self.audit._create_races(db_session)

        assert db_session.query(Faction).count() == 3
        assert db_session.query(Faction).filter_by(name='junk').first() == None

    def test_races_retrieved(self, db_session):
        self.audit._create_races(db_session)

        query = db_session.query(Race)
        races = {r.id : [r.name, r.faction_name] for r in query.all()}

        assert query.count() == len(wow_races['races'])
        assert races[1] == ['Human', 'Alliance']
        assert races[2] == ['Orc', 'Horde']
        assert races[3] == ['Dwarf', 'Alliance']
        assert races[4] == ['Night Elf', 'Alliance']
        assert races[5] == ['Undead', 'Horde']
        assert races[6] == ['Tauren', 'Horde']
        assert races[7] == ['Gnome', 'Alliance']
        assert races[8] == ['Troll', 'Horde']
        assert races[9] == ['Goblin', 'Horde']
        assert races[10] == ['Blood Elf', 'Horde']
        assert races[11] == ['Draenei', 'Alliance']
        assert races[22] == ['Worgen', 'Alliance']
        assert races[24] == ['Pandaren', 'Neutral']
        assert races[25] == ['Pandaren', 'Alliance']
        assert races[26] == ['Pandaren', 'Horde']
        assert races[27] == ['Nightborne', 'Horde']
        assert races[28] == ['Highmountain Tauren', 'Horde']
        assert races[29] == ['Void Elf', 'Alliance']
        assert races[30] == ['Lightforged Draenei', 'Alliance']
        assert races[31] == ['Zandalari Troll', 'Horde']
        assert races[32] == ['Kul Tiran', 'Alliance']
        assert races[34] == ['Dark Iron Dwarf', 'Alliance']
        assert races[36] == ["Mag'har Orc", 'Horde']

    def test_old_races_deleted(self, db_session):
        self.audit._create_races(db_session)

        db_session.add(Race('Voldunai',
            id=14,
            faction=db_session.query(Faction).filter_by(name='Horde').first()))
        db_session.commit()

        self.audit._create_races(db_session)

        assert db_session.query(Race).count() == len(wow_races['races'])
        assert db_session.query(Race).filter_by(name='Voldunai').first() == None

    def test_create_gems(self, db_session):
        self.audit._create_gems(db_session)
        test_gem_id = list(gem_lookup.keys())[0]

        test = db_session.query(Gem).filter_by(id=test_gem_id).first()

        assert test.quality == gem_lookup[test_gem_id]['quality']
        assert test.name == gem_lookup[test_gem_id]['name']
        assert test.icon == gem_lookup[test_gem_id]['icon']
        assert test.stat == gem_lookup[test_gem_id]['stat']

    def test_create_gems_does_not_delete(self, db_session):
        g = Gem(14330, 1, 'Fake Stone', 'inv_fake', '+20 BS')
        db_session.add(g)
        db_session.commit()
        db_session.close()

        self.audit._create_gems(db_session)

        result = db_session.query(Gem).filter_by(id=14330).first()

        assert result != None
        assert result.quality == 1
        assert result.name == 'Fake Stone'
        assert result.icon == 'inv_fake'
        assert result.stat == '+20 BS'

    def test_regions_added(self, db_session):
        self.audit._add_missing_characters(db_session)

        query = db_session.query(Region).all()
        regions = [r.name for r in query]

        assert 'us' in regions
        assert 'eu' in regions

    def test_realms_added(self, db_session):
        self.audit._add_missing_characters(db_session)

        query = db_session.query(Realm).all()
        realms = [{'name' : r.name, 'region' : r.region_name} for r in query]

        assert {'name' : 'kiljaeden', 'region' : 'us'} in realms
        assert {'name' : 'lightbringer', 'region' : 'us'} in realms
        assert {'name' : 'kiljaeden', 'region' : 'eu'} in realms

    def test_characters_added(self, db_session):
        self.audit._add_missing_characters(db_session)

        query = db_session.query(Character).all()
        characters = [{'name' : c.name, 'realm' : c.realm_slug, 'region' : c.region_name} for c in query]

        assert {'name' : 'clegg', 'realm' : 'kiljaeden', 'region' : 'us'} in characters
        assert {'name' : 'salvorhardin', 'realm' : 'kiljaeden', 'region' : 'us'} in characters
        assert {'name' : 'clegg', 'realm' : 'lightbringer', 'region' : 'us'} in characters
        assert {'name' : 'clegg', 'realm' : 'kiljaeden', 'region' : 'eu'} in characters

    def test_remove_old_characters(self, db_session):
        db_session.add(Character('jack',
            realm=db_session.query(Realm).filter_by(name='kiljaeden').first()))
        db_session.commit()

        self.audit._remove_old_characters(db_session)

        assert db_session.query(Character).filter_by(name='jack').first() == None

    def test_add_missing_characters(self, db_session):
        self.audit._add_missing_characters(db_session)

        query = db_session.query(Character).filter_by(name='clegg').join(Realm).filter_by(name='kiljaeden').join(Region).filter_by(name='us')
        clegg = query.first()
        db_session.delete(clegg)
        db_session.commit()

        self.audit._add_missing_characters(db_session)

        assert query.first().name == 'clegg'

    def test_remove_empty_realms(self, db_session):
        db_session.add(Realm('nonexistent'))
        db_session.commit()

        self.audit._remove_empty_realms(db_session)

        assert None == db_session.query(Realm).filter_by(name='nonexistent').first()

    def test_remove_empty_regions(self, db_session):
        db_session.add(Region('nz'))
        db_session.commit()

        self.audit._remove_empty_regions(db_session)

        assert None == db_session.query(Region).filter_by(name='nz').first()

class TestAuditRefresh:
    @classmethod
    def setup_class(cls):
        cls.config = {
                'api' : {
                    'blizzard' : {
                        'client_id' : 'MY_CLIENT_ID',
                        'client_secret' : 'MY_CLIENT_SECRET' },
                    'wcl' : { 'public_key' : 'MY_WCL_KEY' }},
                'characters' : { 'us' : { 'kiljaeden' : ['clegg'] }},
                'database' : 'sqlite://'}

    def setup_method(self, method):
        Utility.year = {}
        Utility.week = {}
        with patch('altaudit.audit.WowApi') as MockApiClass:
            with patch('altaudit.audit.requests.Session') as MockSessionClass:
                def _get_data_resource(url, region):
                    assert region == 'us'
                    for r in wow_races['races']:
                        if url == "{}&{}".format(r['key']['href'], 'locale=en_US'):
                            return wow_race_details[r['id']]

                    assert False, "Race url not found: {}".format(url)

                def _get_playable_race(region, namespace, race_id, locale=None):
                    assert region == 'us'
                    assert namespace == 'static-us'
                    assert locale == 'en_US'
                    return wow_race_details[race_id]

                mock_api = MockApiClass.return_value
                mock_get = MockSessionClass.return_value.get
                mock_api.get_playable_class_index.return_value = wow_classes
                mock_api.get_playable_race_index.return_value = wow_races
                mock_api.get_playable_race.side_effect = _get_playable_race
                mock_api.get_data_resource.side_effect = _get_data_resource
                mock_api.get_character_profile_summary.return_value = { 'last_login_timestamp' : 10 }

                self.mock_blizzard_api = mock_api
                self.mock_get = mock_get

                self.audit = Audit(self.config)
                Base.metadata.create_all(self.audit.engine)
                self.audit.setup_database()

        session = self.audit.make_session()
        chars = session.query(Character).all()

        for c in chars:
            c.lastmodified = 10

        session.commit()
        session.close()

    # TODO mock_process_* have to be included below due to no error handling
    # When better error handling is added these can be removed

    def test_timestamp_set(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize, mocker):
        Utility.set_refresh_timestamp(datetime.datetime.utcnow()) # Prevent update_snapshots from failing
        mock_utility = mocker.patch('altaudit.audit.Utility')
        dt = mocker.MagicMock()
        dt.utcnow.return_value = datetime.datetime(2019, 8, 5)

        self.audit.refresh(dt)

        mock_utility.set_refresh_timestamp.assert_called_once_with(datetime.datetime(2019, 8, 5))

    def test_blizzard_api_called(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        self.audit.refresh(datetime.datetime)
        self.audit.blizzard_api.get_character_profile_summary.assert_called_once_with(region='us', realm_slug='kiljaeden', namespace='profile-us',
                character_name='clegg', locale=BLIZZARD_LOCALE)

    def test_raiderio_called(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):

        self.audit.refresh(datetime.datetime)

        self.mock_get.assert_called_once_with(RAIDERIO_URL.format(
            region='us', realm_slug='kiljaeden', character_name='clegg'))

    def test_character_process_blizzard(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        self.audit.blizzard_api.get_character_profile_summary.return_value = 5

        self.audit.refresh(datetime.datetime)

        mock_process_blizzard.assert_called_once()

    def test_character_process_raiderio(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        self.audit.refresh(datetime.datetime)

        mock_process_raiderio.assert_called_once()

    def test_refresh_returns_list(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        result = self.audit.refresh(datetime.datetime)

        assert result == [Section.metadata('us'), mock_serialize.return_value]

    @pytest.mark.skip(reason='TODO')
    def test_refresh_commits_changes(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        pass

    @pytest.mark.skip(reason='TODO')
    def test_refresh_commit_snapshot_when_process_fails(self, mock_process_blizzard, mock_process_raiderio, mock_update_snapshots, mock_serialize):
        pass
