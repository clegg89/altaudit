"""Unit tests for Azerite info"""
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Class, Character, AzeriteTrait

import altaudit.sections as Section

hoa_item_info = {'id': 158075, 'name': 'Heart of Azeroth', 'icon': 'inv_heartofazeroth', 'quality': 6, 'itemLevel': 427, 'azeriteItem': {'azeriteLevel': 47, 'azeriteExperience': 1062, 'azeriteExperienceRemaining': 22815}}

# Direct output from api. Sorry its hard to read, not easy to clean up
fake_azerite_item_class_powers_in_db = [
    {'powers': [
        {'id': 560, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288802?namespace=static-8.3.0_32861-us'}, 'name': 'Bonded Souls', 'id': 288802}},
        {'id': 127, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/286027?namespace=static-8.3.0_32861-us'}, 'name': 'Equipoise', 'id': 286027}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
        {'id': 128, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272932?namespace=static-8.3.0_32861-us'}, 'name': 'Flames of Alacrity', 'id': 272932}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
        {'id': 132, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272968?namespace=static-8.3.0_32861-us'}, 'name': 'Packed Ice', 'id': 272968}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]},
        {'id': 30, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266180?namespace=static-8.3.0_32861-us'}, 'name': 'Overwhelming Power', 'id': 266180}},
        {'id': 461, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279926?namespace=static-8.3.0_32861-us'}, 'name': 'Earthlink', 'id': 279926}},
        {'id': 21, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263984?namespace=static-8.3.0_32861-us'}, 'name': 'Elemental Whirl', 'id': 263984}},
        {'id': 205, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274379?namespace=static-8.3.0_32861-us'}, 'name': 'Eldritch Warding', 'id': 274379}},
        {'id': 15, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263962?namespace=static-8.3.0_32861-us'}, 'name': 'Resounding Protection', 'id': 263962}},
        {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
        {'id': 214, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274594?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane Pressure', 'id': 274594}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
        {'id': 167, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273326?namespace=static-8.3.0_32861-us'}, 'name': 'Brain Storm', 'id': 273326}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
        {'id': 215, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274596?namespace=static-8.3.0_32861-us'}, 'name': 'Blaster Master', 'id': 274596}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
        {'id': 168, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288755?namespace=static-8.3.0_32861-us'}, 'name': 'Wildfire', 'id': 288755}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
        {'id': 225, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279854?namespace=static-8.3.0_32861-us'}, 'name': 'Glacial Assault', 'id': 279854}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]},
        {'id': 170, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288164?namespace=static-8.3.0_32861-us'}, 'name': 'Flash Freeze', 'id': 288164}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/8?namespace=static-8.3.0_32861-us'}, 'name': 'Mage', 'id': 8}},
    {'powers': [
        {'id': 560, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288802?namespace=static-8.3.0_32861-us'}, 'name': 'Bonded Souls', 'id': 288802}},
        {'id': 113, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272775?namespace=static-8.3.0_32861-us'}, 'name': 'Moment of Repose', 'id': 272775}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
        {'id': 114, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272780?namespace=static-8.3.0_32861-us'}, 'name': 'Permeating Glow', 'id': 272780}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
        {'id': 115, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272788?namespace=static-8.3.0_32861-us'}, 'name': 'Searing Dialogue', 'id': 272788}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]},
        {'id': 30, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266180?namespace=static-8.3.0_32861-us'}, 'name': 'Overwhelming Power', 'id': 266180}},
        {'id': 102, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/267892?namespace=static-8.3.0_32861-us'}, 'name': 'Synergistic Growth', 'id': 267892}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}, {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
        {'id': 42, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/267883?namespace=static-8.3.0_32861-us'}, 'name': 'Savior', 'id': 267883}},
        {'id': 204, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274366?namespace=static-8.3.0_32861-us'}, 'name': 'Sanctum', 'id': 274366}},
        {'id': 15, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263962?namespace=static-8.3.0_32861-us'}, 'name': 'Resounding Protection', 'id': 263962}},
        {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
        {'id': 227, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275541?namespace=static-8.3.0_32861-us'}, 'name': 'Depth of the Shadows', 'id': 275541}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}, {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
        {'id': 164, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273307?namespace=static-8.3.0_32861-us'}, 'name': 'Weal and Woe', 'id': 273307}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
        {'id': 228, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275602?namespace=static-8.3.0_32861-us'}, 'name': 'Prayerful Litany', 'id': 275602}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
        {'id': 165, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273313?namespace=static-8.3.0_32861-us'}, 'name': 'Blessed Sanctuary', 'id': 273313}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
        {'id': 236, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275722?namespace=static-8.3.0_32861-us'}, 'name': 'Whispers of the Damned', 'id': 275722}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]},
        {'id': 166, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288340?namespace=static-8.3.0_32861-us'}, 'name': 'Thought Harvester', 'id': 288340}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/5?namespace=static-8.3.0_32861-us'}, 'name': 'Priest', 'id': 5}},
    {'powers': [
        {'id': 560, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288802?namespace=static-8.3.0_32861-us'}, 'name': 'Bonded Souls', 'id': 288802}},
        {'id': 123, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272891?namespace=static-8.3.0_32861-us'}, 'name': 'Wracking Brilliance', 'id': 272891}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
        {'id': 130, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272944?namespace=static-8.3.0_32861-us'}, 'name': "Shadow's Bite", 'id': 272944}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
        {'id': 131, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/287637?namespace=static-8.3.0_32861-us'}, 'name': 'Chaos Shards', 'id': 287637}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]},
        {'id': 30, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266180?namespace=static-8.3.0_32861-us'}, 'name': 'Overwhelming Power', 'id': 266180}},
        {'id': 461, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279926?namespace=static-8.3.0_32861-us'}, 'name': 'Earthlink', 'id': 279926}},
        {'id': 21, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263984?namespace=static-8.3.0_32861-us'}, 'name': 'Elemental Whirl', 'id': 263984}},
        {'id': 208, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274418?namespace=static-8.3.0_32861-us'}, 'name': 'Lifeblood', 'id': 274418}},
        {'id': 15, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263962?namespace=static-8.3.0_32861-us'}, 'name': 'Resounding Protection', 'id': 263962}},
        {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
        {'id': 230, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275372?namespace=static-8.3.0_32861-us'}, 'name': 'Cascading Calamity', 'id': 275372}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
        {'id': 183, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273521?namespace=static-8.3.0_32861-us'}, 'name': 'Inevitable Demise', 'id': 273521}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
        {'id': 231, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275395?namespace=static-8.3.0_32861-us'}, 'name': 'Explosive Potential', 'id': 275395}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
        {'id': 190, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273523?namespace=static-8.3.0_32861-us'}, 'name': 'Umbral Blaze', 'id': 273523}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
        {'id': 232, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275425?namespace=static-8.3.0_32861-us'}, 'name': 'Flashpoint', 'id': 275425}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]},
        {'id': 460, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279909?namespace=static-8.3.0_32861-us'}, 'name': 'Bursting Flare', 'id': 279909}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/9?namespace=static-8.3.0_32861-us'}, 'name': 'Warlock', 'id': 9}}]

fake_azerite_item_class_powers_not_in_db = {
    '9': [
        {'id': 561, 'tier': 3, 'spellId': 288802},
        {'id': 124, 'tier': 3, 'spellId': 272891},
        {'id': 132, 'tier': 3, 'spellId': 272944},
        {'id': 133, 'tier': 3, 'spellId': 287637},
        {'id': 33, 'tier': 2, 'spellId': 266180},
        {'id': 465, 'tier': 2, 'spellId': 279926},
        {'id': 22, 'tier': 2, 'spellId': 263984},
        {'id': 209, 'tier': 1, 'spellId': 274418},
        {'id': 16, 'tier': 1, 'spellId': 263962},
        {'id': 19, 'tier': 0, 'spellId': 263978},
        {'id': 238, 'tier': 4, 'spellId': 275372},
        {'id': 185, 'tier': 4, 'spellId': 273521},
        {'id': 239, 'tier': 4, 'spellId': 275395},
        {'id': 192, 'tier': 4, 'spellId': 273523},
        {'id': 234, 'tier': 4, 'spellId': 275425},
        {'id': 463, 'tier': 4, 'spellId': 279909}]}

fake_azerite_item_traits_in_db = [
        { 'id' : 13, 'tier' : 0, 'spell_tooltip' :
            { 'spell' : { 'id' : 263978, 'name' : 'Azerite Empowered' }}},
        { 'id' : 15, 'tier' : 1, 'spell_tooltip' :
            { 'spell' : { 'id' : 263962, 'name' : 'Resounding Protection'}}},
        { 'id' : 30, 'tier' : 2, 'spell_tooltip' :
            { 'spell' : { 'id' : 266180, 'name' : 'Overwhelming Power'}}},
        { 'id' : 123, 'tier' : 3, 'spell_tooltip' :
            { 'spell' : { 'id' : 272891, 'name' : 'Wracking Brilliance'}}},
        { 'id' : 183, 'tier' : 4, 'spell_tooltip' :
            { 'spell' : { 'id' : 273521, 'name' : 'Inevitable Demise'}}}]

fake_azerite_item_traits_not_in_db = {
        'id' : 165822,
        'azeriteEmpoweredItem' : { 'azeritePowers' : [
                 {'id': 19, 'tier': 0, 'spellId': 263978},
                 {'id': 16, 'tier': 1, 'spellId': 263962},
                 {'id': 33, 'tier': 2, 'spellId': 266180},
                 {'id': 124, 'tier': 3, 'spellId': 272891},
                 {'id': 185, 'tier': 4, 'spellId': 273521}]}}

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add(Class('Warlock', id=9))

    for trait in fake_azerite_item_class_powers_in_db[2]['powers']:
        session.add(AzeriteTrait(trait['id'], trait['spell']['id'], trait['spell']['name'], ''))

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
def mock_api(mocker):
    mock = mocker.MagicMock()

    mock.get_data_resource.return_value = { 'azerite_class_powers' :
            fake_azerite_item_class_powers_in_db }

    return mock

def test_hoa_info():
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : [{
                'name' : 'Heart of Azeroth',
                'slot' : { 'type' : 'NECK' },
                'azerite_details' : {
                    'percentage_to_next_level' : 0.52,
                    'level' : { 'value' : 61 }}}]}}
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == 61
    assert jack.azerite_percentage == 0.52

def test_hoa_info_no_neck():
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : []}}
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_percentage == None

def test_hoa_info_non_hoa_neck():
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : [{
                'name' : 'Some Other Garbage',
                'slot' : { 'type' : 'NECK' },
                'azerite_details' : {}}]}}
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_percentage == None

def test_azerite_item_in_db(db_session, mock_api):
    jack = Character('jack', class_id=9)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Fake Azerite Name'
    assert jack._head_tier0_selected.icon == 'inv_fake_icon'
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Fake Azerite Name'
    assert jack._head_tier0_available[0].icon == 'inv_fake_icon'
    assert len(jack._head_tier0_available) == 1

def test_azerite_item_not_in_db(db_session, mock_api):
    mock_api.get_item.return_value = { 'azeriteClassPowers' :
            fake_azerite_item_class_powers_not_in_db }

    def _get_spell(region, spellId, locale=None):
        assert region == 'us'
        assert locale == 'en_US'
        return { 'id' : spellId, 'name' : 'Fake Name', 'icon' : 'inv_fake' }

    mock_api.get_spell.side_effect = _get_spell

    jack = Character('jack', class_id=9)
    response = { 'items' : { 'head' : fake_azerite_item_traits_not_in_db } }
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 19
    assert mock_api.get_spell.call_count == 16
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Fake Name'
    assert jack._head_tier0_selected.icon == 'inv_fake'
    assert jack._head_tier0_available[0].id == 19
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Fake Name'
    assert jack._head_tier0_available[0].icon == 'inv_fake'

def test_azerite_item_no_item():
    jack = Character('jack')
    response = { 'items' : {} }

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []

def test_azerite_item_no_traits():
    jack = Character('jack')
    response = { 'items' : { 'head' : { 'id' : 165822, 'azeriteEmpoweredItem' : { 'azeritePowers' : [] } } } }

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []

def test_azerite_no_api_given_set_hoa():
    jack = Character('jack')
    response = { 'items' : {
        'neck' : hoa_item_info,
        'head' : fake_azerite_item_traits_not_in_db,
        }
    }
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == 47
    assert jack.azerite_experience == 1062
    assert jack.azerite_experience_remaining == 22815

def test_azerite_no_api_no_change_traits():
    jack = Character('jack', class_id=9)
    jack._head_tier0_selected = AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard')
    jack._head_tier0_available.append(AzeriteTrait(13, 263978, 'Azerite Empowered', 'inv_smallazeriteshard'))
    response = { 'items' : { 'head' : fake_azerite_item_traits_not_in_db } }
    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == 'inv_smallazeriteshard'
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Azerite Empowered'
    assert jack._head_tier0_available[0].icon == 'inv_smallazeriteshard'
    assert len(jack._head_tier0_available) == 1
