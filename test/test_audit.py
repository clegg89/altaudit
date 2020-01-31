"""Unit Tests for the Audit class"""
import pytest

from unittest.mock import patch

import datetime
from sqlalchemy.orm import sessionmaker

from altaudit.audit import Audit
from altaudit.utility import Utility
from altaudit.models import Base, Faction, Class, Race, Region, Realm, Character, Gem
from altaudit.constants import BLIZZARD_LOCALE, BLIZZARD_CHARACTER_FIELDS, RAIDERIO_URL
from altaudit.gem_enchant import gem_lookup
import altaudit.sections as Section

wow_classes = {'classes': [
    {'id': 1, 'mask': 1, 'powerType': 'rage', 'name': 'Warrior'},
    {'id': 2, 'mask': 2, 'powerType': 'mana', 'name': 'Paladin'},
    {'id': 3, 'mask': 4, 'powerType': 'focus', 'name': 'Hunter'},
    {'id': 4, 'mask': 8, 'powerType': 'energy', 'name': 'Rogue'},
    {'id': 5, 'mask': 16, 'powerType': 'mana', 'name': 'Priest'},
    {'id': 6, 'mask': 32, 'powerType': 'runic-power', 'name': 'Death Knight'},
    {'id': 7, 'mask': 64, 'powerType': 'mana', 'name': 'Shaman'},
    {'id': 8, 'mask': 128, 'powerType': 'mana', 'name': 'Mage'},
    {'id': 9, 'mask': 256, 'powerType': 'mana', 'name': 'Warlock'},
    {'id': 10, 'mask': 512, 'powerType': 'energy', 'name': 'Monk'},
    {'id': 11, 'mask': 1024, 'powerType': 'mana', 'name': 'Druid'},
    {'id': 12, 'mask': 2048, 'powerType': 'fury', 'name': 'Demon Hunter'}]}

wow_races = {'races': [
    {'id': 1, 'mask': 1, 'side': 'alliance', 'name': 'Human'},
    {'id': 2, 'mask': 2, 'side': 'horde', 'name': 'Orc'},
    {'id': 3, 'mask': 4, 'side': 'alliance', 'name': 'Dwarf'},
    {'id': 4, 'mask': 8, 'side': 'alliance', 'name': 'Night Elf'},
    {'id': 5, 'mask': 16, 'side': 'horde', 'name': 'Undead'},
    {'id': 6, 'mask': 32, 'side': 'horde', 'name': 'Tauren'},
    {'id': 7, 'mask': 64, 'side': 'alliance', 'name': 'Gnome'},
    {'id': 8, 'mask': 128, 'side': 'horde', 'name': 'Troll'},
    {'id': 9, 'mask': 256, 'side': 'horde', 'name': 'Goblin'},
    {'id': 10, 'mask': 512, 'side': 'horde', 'name': 'Blood Elf'},
    {'id': 11, 'mask': 1024, 'side': 'alliance', 'name': 'Draenei'},
    {'id': 22, 'mask': 2097152, 'side': 'alliance', 'name': 'Worgen'},
    {'id': 24, 'mask': 8388608, 'side': 'neutral', 'name': 'Pandaren'},
    {'id': 25, 'mask': 16777216, 'side': 'alliance', 'name': 'Pandaren'},
    {'id': 26, 'mask': 33554432, 'side': 'horde', 'name': 'Pandaren'},
    {'id': 27, 'mask': 67108864, 'side': 'horde', 'name': 'Nightborne'},
    {'id': 28, 'mask': 134217728, 'side': 'horde', 'name': 'Highmountain Tauren'},
    {'id': 29, 'mask': 268435456, 'side': 'alliance', 'name': 'Void Elf'},
    {'id': 30, 'mask': 536870912, 'side': 'alliance', 'name': 'Lightforged Draenei'},
    {'id': 31, 'mask': 1073741824, 'side': 'horde', 'name': 'Zandalari Troll'},
    {'id': 32, 'mask': -2147483648, 'side': 'alliance', 'name': 'Kul Tiran'},
    {'id': 34, 'mask': 2, 'side': 'alliance', 'name': 'Dark Iron Dwarf'},
    {'id': 36, 'mask': 8, 'side': 'horde', 'name': "Mag'har Orc"}]}

@pytest.fixture
def mock_session_get(mocker):
    return mocker.patch('altaudit.audit.requests.Session.get')

@pytest.fixture
def mock_process_blizzard(mocker):
    return mocker.patch('altaudit.audit.Character.process_blizzard')

@pytest.fixture
def mock_process_raiderio(mocker):
    return mocker.patch('altaudit.audit.Character.process_raiderio')

@pytest.fixture
def mock_serialize(mocker):
    mock = mocker.patch('altaudit.audit.Character.serialize')
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
                'database' : 'sqlite://',
                'server' : 'localhost:/var/www/html'}

    def setup_method(self, method):
        with patch('altaudit.audit.WowApi') as MockApiClass:
            self.mock_wowapi = MockApiClass
            mock_api = MockApiClass.return_value
            mock_api.get_playable_classes.return_value = wow_classes
            mock_api.get_character_races.return_value = wow_races

            self.mock_blizzard_api = mock_api

            self.audit = Audit(self.config)
            Base.metadata.create_all(self.audit.engine)

    @pytest.fixture
    def db_session(self):
        session = sessionmaker(self.audit.engine)()
        yield session
        session.close()

    def test_engine_created(self):
        assert self.audit.engine.name == 'sqlite'

    def test_blizzard_api_created(self):
        self.mock_wowapi.assert_called_once_with(client_id='MY_CLIENT_ID',
                client_secret='MY_CLIENT_SECRET', retry_conn_failures=False)

    @pytest.mark.skip(reason='Unnecessary, should be checked where server is used')
    def test_server(self):
        assert self.audit.server == self.config['server']

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

    def test_factions_made(self, db_session):
        self.audit._create_factions(db_session)

        query = db_session.query(Faction)
        factions = {f.id : f.name for f in query.all()}

        assert query.count() == 3
        assert factions[1] == 'Alliance'
        assert factions[2] == 'Horde'
        assert factions[3] == 'Neutral'

    def test_factions_remade(self, db_session):
        self.audit._create_factions(db_session)

        db_session.add(Faction('junk', id=4))
        db_session.commit()

        self.audit._create_factions(db_session)

        assert db_session.query(Faction).count() == 3
        assert db_session.query(Faction).filter_by(name='junk').first() == None

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

    def test_races_retrieved(self, db_session):
        self.audit._create_factions(db_session)
        self.audit._create_races(db_session)

        query = db_session.query(Race)
        races = {r.id : [r.name, r.faction_name] for r in query.all()}

        assert query.count() == 23
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
        self.audit._create_factions(db_session)
        self.audit._create_races(db_session)

        db_session.add(Race('Voldunai',
            id=14,
            faction=db_session.query(Faction).filter_by(name='Horde').first()))
        db_session.commit()

        self.audit._create_races(db_session)

        assert db_session.query(Race).count() == 23
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
                'database' : 'sqlite://',
                'server' : 'localhost:/var/www/html'}

    def setup_method(self, method):
        Utility.year = {}
        Utility.week = {}
        with patch('altaudit.audit.WowApi') as MockApiClass:
            with patch('altaudit.audit.requests.Session') as MockSessionClass:
                mock_api = MockApiClass.return_value
                mock_get = MockSessionClass.return_value.get
                mock_api.get_playable_classes.return_value = wow_classes
                mock_api.get_character_races.return_value = wow_races
                mock_api.get_character_profile.return_value = { 'lastModified' : 10 }

                self.mock_blizzard_api = mock_api
                self.mock_get = mock_get

                self.audit = Audit(self.config)
                Base.metadata.create_all(self.audit.engine)
                self.audit.setup_database()

        session = sessionmaker(self.audit.engine)()
        chars = session.query(Character).all()

        for c in chars:
            c.lastmodified = 10

        session.commit()
        session.close()

    # TODO mock_process_* have to be included below due to no error handling
    # When better error handling is added these can be removed

    def test_timestamp_set(self, mock_process_blizzard, mock_process_raiderio, mock_serialize, mocker):
        Utility.set_refresh_timestamp(datetime.datetime.utcnow()) # Prevent update_snapshots from failing
        mock_utility = mocker.patch('altaudit.audit.Utility')
        dt = mocker.MagicMock()
        dt.utcnow.return_value = datetime.datetime(2019, 8, 5)

        self.audit.refresh(dt)

        mock_utility.set_refresh_timestamp.assert_called_once_with(datetime.datetime(2019, 8, 5))

    def test_blizzard_api_called(self, mock_process_blizzard, mock_process_raiderio, mock_serialize):
        self.audit.refresh(datetime.datetime)
        self.audit.blizzard_api.get_character_profile.assert_called_once_with(region='us', realm='kiljaeden',
                character_name='clegg', locale=BLIZZARD_LOCALE,
                fields=','.join(BLIZZARD_CHARACTER_FIELDS))

    def test_raiderio_called(self, mock_process_blizzard, mock_process_raiderio, mock_serialize):

        self.audit.refresh(datetime.datetime)

        self.mock_get.assert_called_once_with(RAIDERIO_URL.format(
            region='us', realm='kiljaeden', character_name='clegg'))

    def test_character_process_blizzard(self, mock_process_blizzard, mock_process_raiderio, mock_serialize):
        self.audit.blizzard_api.get_character_profile.return_value = 5

        self.audit.refresh(datetime.datetime)

        mock_process_blizzard.assert_called_once()

    def test_character_process_raiderio(self, mock_process_blizzard, mock_process_raiderio, mock_serialize):
        self.audit.refresh(datetime.datetime)

        mock_process_raiderio.assert_called_once()

    def test_refresh_returns_list(self, mock_process_blizzard, mock_process_raiderio, mock_serialize):
        result = self.audit.refresh(datetime.datetime)

        assert result == [Section.metadata(), mock_serialize.return_value]

    def tes_refresh_commit_data(self, mock_process_blizzard, mock_process_raiderio, mock_serialize, mocker):
        mock_commit = mocker.patch('altaudit.audit.sqlalchemy.orm.session.Session.commit')
        self.audit.refresh(datetime.datetime)
        mock_commit.assert_called_once()
