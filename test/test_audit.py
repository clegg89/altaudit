"""Unit Tests for the Audit class"""
import pytest

from sqlalchemy.orm import sessionmaker

from charfetch.audit import Audit

from charfetch.models import Faction

@pytest.fixture
def mock_blizzard_api(mocker):
    return mocker.patch('charfetch.audit.WowApi')

@pytest.mark.usefixtures('mock_blizzard_api')
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
        alliance = db_session.query(Faction).filter_by(name='alliance').first()
        horde = db_session.query(Faction).filter_by(name='horde').first()
        neutral = db_session.query(Faction).filter_by(name='neutral').first()

        assert db_session.query(Faction).count() == 3
        assert alliance.id == 1
        assert horde.id == 2
        assert neutral.id == 3
