"""Unit Tests for basic info"""
import pytest

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, Class, Faction, Race

import altaudit.sections.basic as Section

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
    session.add_all([Class(c['name'], id=c['id']) for c in classes['classes']])
    session.add_all([Race(r['name'], id=r['id'],
        faction=session.query(Faction).filter_by(name=r['faction']['name']).first())
        for r in races])

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
    def _maker(
            name='toon1',
            gender='Male',
            race_name='Undead',
            class_name='Warlock',
            mainspec='Destruction',
            realm='realm1',
            level=120,
            timestamp=int(datetime.datetime.now().timestamp())*1000,
            avatar='avatar_url',
            bust='bust_url',
            render='render_url'):
        class_id = next(c['id'] for c in classes['classes'] if c['name'] == class_name)
        race = next(r for r in races if r['name'] == race_name)
        race_id = race['id']
        faction = race['faction']['name']
        gender in ('Male','Female')

        return { 'summary' : {
                'name' : name,
                'gender' : { 'type' : gender.upper(), 'name' : gender },
                'faction' : { 'type' : faction.upper(), 'name' : faction },
                'race' : { 'name' : race_name, 'id' : race_id },
                'character_class' : { 'name' : class_name, 'id' : class_id },
                'active_spec' : { 'name' : mainspec },
                'realm' : { 'name' : realm },
                'level' : level,
                'last_login_timestamp' : timestamp },
            'media' : {
                'assets' : [
                    { 'key' : 'avatar', 'value' : avatar },
                    { 'key' : 'inset', 'value' : bust },
                    { 'key' : 'main', 'value' : render }]}
            }

    return _maker

def test_basic_info_name(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(name='Jack')
    Section.basic(jack, response, db_session)
    assert jack.name_api == 'Jack'

def test_basic_info_gender(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(gender='Female')
    Section.basic(jack, response, db_session)
    assert jack.gender == 'Female'

def test_basic_info_faction(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    Section.basic(jack, response, db_session)
    assert type(jack.faction) == Faction
    assert jack.faction.name == 'Horde'

def test_basic_info_race(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(race_name="Undead")
    Section.basic(jack, response, db_session)
    assert type(jack.race) == Race
    assert jack.race.name == "Undead"
    assert jack.race.id == 5

def test_basic_info_class(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(class_name='Monk')
    Section.basic(jack, response, db_session)
    assert type(jack.character_class) == Class
    assert jack.character_class.name == 'Monk'
    assert jack.character_class.id == 10

def test_basic_info_mainspec(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(mainspec='Shadow')
    Section.basic(jack, response, db_session)
    assert jack.mainspec == 'Shadow'

def test_basic_info_mainspec_not_present(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker()
    del response['summary']['active_spec']
    Section.basic(jack, response, db_session)
    assert jack.mainspec == None

def test_basic_info_realm(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(realm="Zin'azshara")
    Section.basic(jack, response, db_session)
    assert jack.realm_name == "Zin'azshara"

def test_basic_info_level(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(level=45)
    Section.basic(jack, response, db_session)
    assert jack.level == 45

def test_basic_info_timestamp(fake_response_maker, db_session):
    jack = Character('jack')
    now = datetime.datetime.now().timestamp()*1000
    response = fake_response_maker(timestamp=now)
    Section.basic(jack, response, db_session)
    assert jack.lastmodified == now

def test_basic_info_avatar(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(avatar='realm1/96/184987488-avatar.jpg')
    Section.basic(jack, response, db_session)
    assert jack.avatar == 'realm1/96/184987488-avatar.jpg'

def test_basic_info_bust(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(bust='realm1/96/184987488-inset.jpg')
    Section.basic(jack, response, db_session)
    assert jack.bust == 'realm1/96/184987488-inset.jpg'

def test_basic_info_render(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(render='realm1/96/184987488-main.jpg')
    Section.basic(jack, response, db_session)
    assert jack.render == 'realm1/96/184987488-main.jpg'

def test_basic_info_avatar_old(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(avatar='realm1/96/184987488-avatar.jpg')
    response['media'] = {
            'avatar_url' : 'realm1/96/184987488-avatar.jpg',
            'bust_url' : 'bust_url',
            'render_url' : 'render_url'}
    Section.basic(jack, response, db_session)
    assert jack.avatar == 'realm1/96/184987488-avatar.jpg'

def test_basic_info_bust_old(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(bust='realm1/96/184987488-inset.jpg')
    response['media'] = {
            'avatar_url' : 'avatar_url',
            'bust_url' : 'realm1/96/184987488-inset.jpg',
            'render_url' : 'render_url'}
    Section.basic(jack, response, db_session)
    assert jack.bust == 'realm1/96/184987488-inset.jpg'

def test_basic_info_render_old(fake_response_maker, db_session):
    jack = Character('jack')
    response = fake_response_maker(render='realm1/96/184987488-main.jpg')
    response['media'] = {
            'avatar_url' : 'avatar_url',
            'bust_url' : 'bust_url',
            'render_url' : 'realm1/96/184987488-main.jpg'}
    Section.basic(jack, response, db_session)
    assert jack.render == 'realm1/96/184987488-main.jpg'
