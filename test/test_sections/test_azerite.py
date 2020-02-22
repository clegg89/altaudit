"""Unit tests for Azerite info"""
import pytest

import copy

from wowapi import WowApiException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Base, Class, Character, AzeriteTrait

import altaudit.sections.azerite as Section

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

# Direct output from api. Sorry its hard to read, not easy to clean up
fake_azerite_item_class_powers_not_in_db  = [
        {'powers': [
            {'id': 193, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273823?namespace=static-8.3.0_32861-us'}, 'name': 'Blightborne Infusion', 'id': 273823}},
            {'id': 374, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278536?namespace=static-8.3.0_32861-us'}, 'name': 'Galvanizing Spark', 'id': 278536}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
            {'id': 128, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272932?namespace=static-8.3.0_32861-us'}, 'name': 'Flames of Alacrity', 'id': 272932}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
            {'id': 381, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278542?namespace=static-8.3.0_32861-us'}, 'name': 'Frigid Grasp', 'id': 278542}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]},
            {'id': 462, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266936?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Globules', 'id': 266936}},
            {'id': 22, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263987?namespace=static-8.3.0_32861-us'}, 'name': 'Heed My Call', 'id': 263987}},
            {'id': 459, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279899?namespace=static-8.3.0_32861-us'}, 'name': 'Unstable Flames', 'id': 279899}},
            {'id': 468, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/280015?namespace=static-8.3.0_32861-us'}, 'name': 'Cauterizing Blink', 'id': 280015}},
            {'id': 14, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/268594?namespace=static-8.3.0_32861-us'}, 'name': 'Longstrider', 'id': 268594}},
            {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
            {'id': 167, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273326?namespace=static-8.3.0_32861-us'}, 'name': 'Brain Storm', 'id': 273326}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
            {'id': 214, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274594?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane Pressure', 'id': 274594}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/62?namespace=static-8.3.0_32861-us'}, 'name': 'Arcane', 'id': 62}]},
            {'id': 168, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288755?namespace=static-8.3.0_32861-us'}, 'name': 'Wildfire', 'id': 288755}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
            {'id': 215, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/274596?namespace=static-8.3.0_32861-us'}, 'name': 'Blaster Master', 'id': 274596}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/63?namespace=static-8.3.0_32861-us'}, 'name': 'Fire', 'id': 63}]},
            {'id': 170, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288164?namespace=static-8.3.0_32861-us'}, 'name': 'Flash Freeze', 'id': 288164}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]},
            {'id': 225, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279854?namespace=static-8.3.0_32861-us'}, 'name': 'Glacial Assault', 'id': 279854}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/64?namespace=static-8.3.0_32861-us'}, 'name': 'Frost', 'id': 64}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/8?namespace=static-8.3.0_32861-us'}, 'name': 'Mage', 'id': 8}},
        {'powers': [
            {'id': 193, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273823?namespace=static-8.3.0_32861-us'}, 'name': 'Blightborne Infusion', 'id': 273823}},
            {'id': 398, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278629?namespace=static-8.3.0_32861-us'}, 'name': 'Contemptuous Homily', 'id': 278629}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
            {'id': 114, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272780?namespace=static-8.3.0_32861-us'}, 'name': 'Permeating Glow', 'id': 272780}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
            {'id': 405, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278661?namespace=static-8.3.0_32861-us'}, 'name': 'Chorus of Insanity', 'id': 278661}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]},
            {'id': 462, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266936?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Globules', 'id': 266936}},
            {'id': 103, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/267882?namespace=static-8.3.0_32861-us'}, 'name': 'Concentrated Mending', 'id': 267882}},
            {'id': 105, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/267886?namespace=static-8.3.0_32861-us'}, 'name': 'Ephemeral Recovery', 'id': 267886}},
            {'id': 472, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/280018?namespace=static-8.3.0_32861-us'}, 'name': 'Twist Magic', 'id': 280018}},
            {'id': 14, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/268594?namespace=static-8.3.0_32861-us'}, 'name': 'Longstrider', 'id': 268594}},
            {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
            {'id': 164, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273307?namespace=static-8.3.0_32861-us'}, 'name': 'Weal and Woe', 'id': 273307}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
            {'id': 227, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275541?namespace=static-8.3.0_32861-us'}, 'name': 'Depth of the Shadows', 'id': 275541}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}, {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/256?namespace=static-8.3.0_32861-us'}, 'name': 'Discipline', 'id': 256}]},
            {'id': 165, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273313?namespace=static-8.3.0_32861-us'}, 'name': 'Blessed Sanctuary', 'id': 273313}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
            {'id': 228, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275602?namespace=static-8.3.0_32861-us'}, 'name': 'Prayerful Litany', 'id': 275602}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/257?namespace=static-8.3.0_32861-us'}, 'name': 'Holy', 'id': 257}]},
            {'id': 166, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/288340?namespace=static-8.3.0_32861-us'}, 'name': 'Thought Harvester', 'id': 288340}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]},
            {'id': 236, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275722?namespace=static-8.3.0_32861-us'}, 'name': 'Whispers of the Damned', 'id': 275722}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/258?namespace=static-8.3.0_32861-us'}, 'name': 'Shadow', 'id': 258}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/5?namespace=static-8.3.0_32861-us'}, 'name': 'Priest', 'id': 5}},
        {'powers': [
            {'id': 193, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273823?namespace=static-8.3.0_32861-us'}, 'name': 'Blightborne Infusion', 'id': 273823}},
            {'id': 425, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278721?namespace=static-8.3.0_32861-us'}, 'name': 'Sudden Onset', 'id': 278721}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
            {'id': 130, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/272944?namespace=static-8.3.0_32861-us'}, 'name': "Shadow's Bite", 'id': 272944}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
            {'id': 432, 'tier': 3, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/278748?namespace=static-8.3.0_32861-us'}, 'name': 'Chaotic Inferno', 'id': 278748}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]},
            {'id': 462, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/266936?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Globules', 'id': 266936}},
            {'id': 22, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263987?namespace=static-8.3.0_32861-us'}, 'name': 'Heed My Call', 'id': 263987}},
            {'id': 459, 'tier': 2, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279899?namespace=static-8.3.0_32861-us'}, 'name': 'Unstable Flames', 'id': 279899}},
            {'id': 475, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/280022?namespace=static-8.3.0_32861-us'}, 'name': 'Desperate Power', 'id': 280022}},
            {'id': 14, 'tier': 1, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/268594?namespace=static-8.3.0_32861-us'}, 'name': 'Longstrider', 'id': 268594}},
            {'id': 13, 'tier': 0, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/263978?namespace=static-8.3.0_32861-us'}, 'name': 'Azerite Empowered', 'id': 263978}},
            {'id': 183, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273521?namespace=static-8.3.0_32861-us'}, 'name': 'Inevitable Demise', 'id': 273521}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
            {'id': 230, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275372?namespace=static-8.3.0_32861-us'}, 'name': 'Cascading Calamity', 'id': 275372}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/265?namespace=static-8.3.0_32861-us'}, 'name': 'Affliction', 'id': 265}]},
            {'id': 190, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/273523?namespace=static-8.3.0_32861-us'}, 'name': 'Umbral Blaze', 'id': 273523}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
            {'id': 231, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275395?namespace=static-8.3.0_32861-us'}, 'name': 'Explosive Potential', 'id': 275395}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/266?namespace=static-8.3.0_32861-us'}, 'name': 'Demonology', 'id': 266}]},
            {'id': 460, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/279909?namespace=static-8.3.0_32861-us'}, 'name': 'Bursting Flare', 'id': 279909}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]},
            {'id': 232, 'tier': 4, 'spell': {'key': {'href': 'https://us.api.blizzard.com/data/wow/spell/275425?namespace=static-8.3.0_32861-us'}, 'name': 'Flashpoint', 'id': 275425}, 'allowed_specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/267?namespace=static-8.3.0_32861-us'}, 'name': 'Destruction', 'id': 267}]}],
        'playable_class': {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/9?namespace=static-8.3.0_32861-us'}, 'name': 'Warlock', 'id': 9}}]

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

fake_azerite_item_traits_not_in_db  = [
        { 'id' : 13, 'tier' : 0, 'spell_tooltip' :
            { 'spell' : { 'id' : 263978, 'name' : 'Azerite Empowered' }}},
        { 'id' : 14, 'tier' : 1, 'spell_tooltip' :
            { 'spell' : { 'id' : 268594, 'name' : 'Longstrider'}}},
        { 'id' : 22, 'tier' : 2, 'spell_tooltip' :
            { 'spell' : { 'id' : 263987, 'name' : 'Head My Call'}}},
        { 'id' : 425, 'tier' : 3, 'spell_tooltip' :
            { 'spell' : { 'id' : 278721, 'name' : 'Sudden Onset'}}},
        { 'id' : 183, 'tier' : 4, 'spell_tooltip' :
            { 'spell' : { 'id' : 273521, 'name' : 'Inevitable Demise'}}}]

@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)()

    session.add(Class('Warlock', id=9))

    for trait in fake_azerite_item_class_powers_in_db[2]['powers']:
        session.add(AzeriteTrait(trait['id'], trait['spell']['id'], trait['spell']['name'], None))

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
            copy.deepcopy(fake_azerite_item_class_powers_in_db) }

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

def test_hoa_info_hoa_no_azerite_details():
    # Not sure how patch 9.0 will go. Be safe
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : [{
                'name' : 'Heart of Azeroth',
                'slot' : { 'type' : 'NECK' }}]}}
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_percentage == None

def test_hoa_info_hoa_no_level():
    # Not sure how patch 9.0 will go. Be safe
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : [{
                'name' : 'Heart of Azeroth',
                'slot' : { 'type' : 'NECK' },
                'azerite_details' : {'percentage_to_next_level' : 0.52}}]}}
    Section.azerite(jack, response, None, None)
    assert jack.hoa_level == None
    assert jack.azerite_percentage == None

def test_azerite_item_in_db(db_session, mock_api):
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Azerite Empowered'
    assert jack._head_tier0_available[0].icon == None
    assert len(jack._head_tier0_available) == 1

def test_azerite_item_not_in_db(db_session, mock_api):
    mock_api.get_data_resource.return_value = { 'azerite_class_powers' :
            fake_azerite_item_class_powers_not_in_db }

    # Preserving for demonstration
    # def _get_spell(region, spellId, locale=None):
    #     assert region == 'us'
    #     assert locale == 'en_US'
    #     return { 'id' : spellId, 'name' : 'Fake Name', 'icon' : 'inv_fake' }

    # mock_api.get_spell.side_effect = _get_spell

    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_not_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    # assert mock_api.get_spell.call_count == 16
    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert jack._head_tier1_selected.name == 'Longstrider'
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Azerite Empowered'
    assert jack._head_tier0_available[0].icon == None
    assert len(jack._head_tier0_available) == 1

def test_azerite_item_no_item():
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : []}}

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []

def test_azerite_item_no_traits():
    jack = Character('jack')
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' }}]}}

    Section.azerite(jack, response, None, None)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available == []

def test_azerite_item_no_selected_traits(db_session, mock_api):
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : None}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected == None
    assert jack._head_tier0_available[0].id == 13
    assert jack._head_tier0_available[0].spell_id == 263978
    assert jack._head_tier0_available[0].name == 'Azerite Empowered'
    assert jack._head_tier0_available[0].icon == None
    assert len(jack._head_tier0_available) == 1

def test_azerite_item_wow_api_exception(db_session, mock_api):
    mock_api.get_data_resource.side_effect = WowApiException()
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert jack._head_tier0_available == []

def test_azerite_item_item_is_illformed(db_session, mock_api):
    del mock_api.get_data_resource.return_value['azerite_class_powers']
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert jack._head_tier0_available == []

def test_azerite_item_trait_id_is_missing(db_session, mock_api):
    del mock_api.get_data_resource.return_value['azerite_class_powers'][2]['powers'][0]['id']
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db}}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert jack._head_tier3_available[0] == None

def test_azerite_item_trait_tier_is_missing(db_session, mock_api):
    del mock_api.get_data_resource.return_value['azerite_class_powers'][2]['powers'][0]['tier']
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_in_db}}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert len(jack._head_tier3_available) == 3

def test_azerite_item_trait_is_None(db_session, mock_api):
    mock_api.get_data_resource.return_value['azerite_class_powers'][2]['powers'][0] = None
    warlock = db_session.query(Class).filter_by(name='Warlock').first()
    jack = Character('jack', character_class=warlock)
    response = { 'equipment' :
            { 'equipped_items' : [{
                'item' : {'key':{'href' : 'garbage'}},
                'slot' : { 'type' : 'HEAD' },
                'azerite_details' : {
                    'selected_powers' : fake_azerite_item_traits_not_in_db }}]}}
    Section.azerite(jack, response, db_session, mock_api)

    assert jack._head_tier0_selected.id == 13
    assert jack._head_tier0_selected.spell_id == 263978
    assert jack._head_tier0_selected.name == 'Azerite Empowered'
    assert jack._head_tier0_selected.icon == None
    assert len(jack._head_tier3_available) == 3
