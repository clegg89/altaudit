"""Unit Tests for the Audit class"""
import pytest

from unittest.mock import patch

from sqlalchemy.orm import sessionmaker

from charfetch.audit import Audit

from charfetch.models import Faction, Class, Race

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

class TestAuditInit:
    @classmethod
    def setup_class(cls):
        cls.config = {
                'api' : { 'blizzard' : {
                    'client_id' : 'MY_CLIENT_ID',
                    'client_secret' : 'MY_CLIENT_SECRET' }},
                'characters' : {
                    'us' : {
                        'kiljaeden' : [
                            'clegg', 'salvorhardin', 'darksidemoon'],
                        'lightbringer' : [
                            'clegg', 'klegg', 'ingsok']},
                    'eu' : {
                        'argentdawn' : [
                            'tali', 'jack', 'bill']}},
                'database' : 'sqlite://',
                'server' : 'localhost:/var/www/html'}

    def setup_method(self, method):
        with patch('charfetch.audit.WowApi') as MockApiClass:
            mock_api = MockApiClass.return_value
            mock_api.get_character_classes.return_value = wow_classes
            mock_api.get_character_races.return_value = wow_races

            self.mock_blizzard_api = mock_api

            self.audit = Audit(self.config)

    @pytest.fixture
    def db_session(self):
        session = sessionmaker(self.audit.engine)()
        yield session
        session.close()

    def test_engine_created(self):
        assert self.audit.engine.name == 'sqlite'

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
        query = db_session.query(Faction)

        assert query.count() == 3
        assert query.filter_by(id=1).first().name == 'Alliance'
        assert query.filter_by(id=2).first().name == 'Horde'
        assert query.filter_by(id=3).first().name == 'Neutral'

    def test_classes_retrieved(self, db_session):
        query = db_session.query(Class)

        assert query.count() == 12
        assert query.filter_by(id=1).first().name == 'Warrior'
        assert query.filter_by(id=2).first().name == 'Paladin'
        assert query.filter_by(id=3).first().name == 'Hunter'
        assert query.filter_by(id=4).first().name == 'Rogue'
        assert query.filter_by(id=5).first().name == 'Priest'
        assert query.filter_by(id=6).first().name == 'Death Knight'
        assert query.filter_by(id=7).first().name == 'Shaman'
        assert query.filter_by(id=8).first().name == 'Mage'
        assert query.filter_by(id=9).first().name == 'Warlock'
        assert query.filter_by(id=10).first().name == 'Monk'
        assert query.filter_by(id=11).first().name == 'Druid'
        assert query.filter_by(id=12).first().name == 'Demon Hunter'

    def test_races_retrieved(self, db_session):
        query = db_session.query(Race)
        races = {f.id : [f.name, f.faction_name] for f in query.all()}

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
