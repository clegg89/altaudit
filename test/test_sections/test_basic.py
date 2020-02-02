"""Unit Tests for basic info"""
import pytest

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, Class, Faction, Race

import altaudit.sections as Section

classes = {'classes': [
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

factions = ['Alliance', 'Horde', 'Neutral']

races = [
    {'id': 1, 'name': 'Human', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 2, 'name': 'Orc', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 3, 'name': 'Dwarf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 4, 'name': 'Night Elf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 5, 'name': 'Undead', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 6, 'name': 'Tauren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 7, 'name': 'Gnome', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 8, 'name': 'Troll', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 9, 'name': 'Goblin', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 10, 'name': 'Blood Elf', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 11, 'name': 'Draenei', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 22, 'name': 'Worgen', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 24, 'name': 'Pandaren', 'faction': {'type': 'NEUTRAL', 'name': 'Neutral'}, 'is_selectable': True, 'is_allied_race': False},
    {'id': 25, 'name': 'Pandaren', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': False, 'is_allied_race': False},
    {'id': 26, 'name': 'Pandaren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': False, 'is_allied_race': False},
    {'id': 27, 'name': 'Nightborne', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 28, 'name': 'Highmountain Tauren', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 29, 'name': 'Void Elf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 30, 'name': 'Lightforged Draenei', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 31, 'name': 'Zandalari Troll', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 32, 'name': 'Kul Tiran', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 34, 'name': 'Dark Iron Dwarf', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 35, 'name': 'Vulpera', 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 36, 'name': "Mag'har Orc", 'faction': {'type': 'HORDE', 'name': 'Horde'}, 'is_selectable': True, 'is_allied_race': True},
    {'id': 37, 'name': 'Mechagnome', 'faction': {'type': 'ALLIANCE', 'name': 'Alliance'}, 'is_selectable': True, 'is_allied_race': True}]

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add_all([Faction(f) for f in factions])
    session.add_all([Class(c['name'], id=c['id']) for c in classes])
    session.add_all([Race(r['name'], id=r['id'],
        faction=session.query(Faction).filter_by(name=r['faction']['name']).first())
        for r in races)

    session.commit()
    session.close()

    yield engine

    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db):
    session = sessionmaker(db)()
    yield session
    session.close()

@pytest.fixture
def fake_response_maker():
    def _maker(name='toon1', realm='realm1',
            timestamp=int(datetime.datetime.now().timestamp())*1000,
            kls=9, race=34, gender=0, level=120, mainspec='Destruction',
            media_url='184987488'):
        assert kls < len(classes)
        assert race in races
        assert gender in (0,1)

        faction = 0 if races[race]['side'] == 'alliance' else 1 if races[race]['side'] == 'horde' else 2

        return {
                'name' : name,
                'gender' : { 'type' : gender.upper(), 'name' : gender }
                'faction' : { 'type' : faction.upper(), 'name' : faction }
                'race' : { 'name' : race_name, 'id' : race_id }
                'character_class' : { 'name' : class_name, 'id' : class_id }
                'active_spec'

                'lastModified' : timestamp,
                'realm' : realm,
                'level' : level,
                'thumbnail' : '{0}/96/{1}-avatar.jpg'.format(realm, media_url),
                'talents' : [
                    { 'selected' : True, 'spec' : { 'name' : mainspec } },
                    { 'selected' : False, 'spec' : { 'name' : 'Failed' } },
                    { 'selected' : False, 'spec' : { 'name' : 'Failed' } }]}

    return _maker

def test_basic_info_name(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(name='Jack')
    Section.basic(jack, response, db_session)
    assert jack.name_api == 'Jack'

def test_basic_info_realm(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(realm="Zin'azshara")
    Section.basic(jack, response, db_session)
    assert jack.realm_name == "Zin'azshara"

def test_basic_info_timestamp(fake_response_maker, db_session):
    jack = Character('jack')
    now = datetime.datetime.now().timestamp()*1000
    response = fake_response_maker(timestamp=now)
    Section.basic(jack, response, db_session)
    assert jack.lastmodified == now

def test_basic_info_class(fake_response_maker, db_session):
    jack = Character('jack')
    kls = 10
    response = fake_response_maker(kls=kls)
    Section.basic(jack, response, db_session)
    assert jack.class_name == 'Monk'

def test_basic_info_level(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(level=45)
    Section.basic(jack, response, db_session)
    assert jack.level == 45

def test_basic_info_mainspec(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(mainspec='Shadow')
    Section.basic(jack, response, db_session)
    assert jack.mainspec == 'Shadow'

def test_basic_info_faction(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    Section.basic(jack, response, db_session)
    assert jack.faction_name == 'Alliance'

def test_basic_info_gender(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(gender=1)
    Section.basic(jack, response, db_session)
    assert jack.gender == 'Female'

def test_basic_info_race(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(race=32)
    Section.basic(jack, response, db_session)
    assert jack.race_name == "Kul Tiran"

def test_basic_info_avatar(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    Section.basic(jack, response, db_session)
    assert jack.avatar == 'realm1/96/184987488-avatar.jpg'

def test_basic_info_bust(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    Section.basic(jack, response, db_session)
    assert jack.bust == 'realm1/96/184987488-inset.jpg'

def test_basic_info_render(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    Section.basic(jack, response, db_session)
    assert jack.render == 'realm1/96/184987488-main.jpg'
