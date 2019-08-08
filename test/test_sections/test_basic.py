"""Unit Tests for basic info"""
import pytest

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Character, Class, Faction, Race

import altaudit.sections as Section

classes = ['Warrior', 'Paladin', 'Hunter',
    'Rogue', 'Priest', 'Death Knight', 'Shaman',
    'Mage', 'Warlock', 'Monk', 'Druid', 'Demon Hunter']

factions = ['Alliance', 'Horde', 'Neutral']

races = {
    1 : { 'side': 'alliance', 'name': 'Human'},
    2 : { 'side': 'horde', 'name': 'Orc'},
    3 : { 'side': 'alliance', 'name': 'Dwarf'},
    4 : { 'side': 'alliance', 'name': 'Night Elf'},
    5 : { 'side': 'horde', 'name': 'Undead'},
    6 : { 'side': 'horde', 'name': 'Tauren'},
    7 : { 'side': 'alliance', 'name': 'Gnome'},
    8 : { 'side': 'horde', 'name': 'Troll'},
    9 : { 'side': 'horde', 'name': 'Goblin'},
    10 : { 'side': 'horde', 'name': 'Blood Elf'},
    11 : { 'side': 'alliance', 'name': 'Draenei'},
    22 : { 'side': 'alliance', 'name': 'Worgen'},
    24 : { 'side': 'neutral', 'name': 'Pandaren'},
    25 : { 'side': 'alliance', 'name': 'Pandaren'},
    26 : { 'side': 'horde', 'name': 'Pandaren'},
    27 : { 'side': 'horde', 'name': 'Nightborne'},
    28 : { 'side': 'horde', 'name': 'Highmountain Tauren'},
    29 : { 'side': 'alliance', 'name': 'Void Elf'},
    30 : { 'side': 'alliance', 'name': 'Lightforged Draenei'},
    31 : { 'side': 'horde', 'name': 'Zandalari Troll'},
    32 : { 'side': 'alliance', 'name': 'Kul Tiran'},
    34 : { 'side': 'alliance', 'name': 'Dark Iron Dwarf'},
    36 : { 'side': 'horde', 'name': "Mag'har Orc"}}

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add_all([Faction(f, id=i+1) for i,f in enumerate(factions)])
    session.add_all([Class(c, id=i+1) for i,c in enumerate(classes)])
    session.add_all([Race(r['name'], id=i,
        faction=session.query(Faction).filter_by(name=r['side'].capitalize()).first())
        for i,r in races.items()])

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
                'lastModified' : timestamp,
                'name' : name,
                'realm' : realm,
                'class' : kls,
                'race' : race,
                'faction' : faction,
                'gender' : gender,
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
