"""Unit Tests for the sections utilities"""
import pytest

from altaudit.sections.utility import is_off_hand_weapon, is_primary_enchant_slot

def test_not_weapon_if_two_handed_not_fury_warrior():
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Warlock' },
                'active_spec' : { 'name' : 'Destruction' }},
            'equipment' : { 'equipped_items' : [{
                'slot' : { 'type' : 'MAIN_HAND' },
                'inventory_type' : { 'type' : 'TWOHWEAPON' },
                'item_subclass' : { 'name' : 'Axe' }}]}}

    assert False == is_off_hand_weapon(profile)

def test_is_weapon_if_not_two_handed():
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Rogue' },
                'active_spec' : { 'name' : 'Outlaw' }},
            'equipment' : { 'equipped_items' : [{
                'slot' : { 'type' : 'MAIN_HAND' },
                'inventory_type' : { 'type' : 'WEAPON' },
                'item_subclass' : { 'name' : 'Axe' }}]}}

    assert True == is_off_hand_weapon(profile)

def test_is_weapon_if_two_handed_and_fury_warrior():
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Warrior' },
                'active_spec' : { 'name' : 'Fury' }},
            'equipment' : { 'equipped_items' : [{
                'slot' : { 'type' : 'MAIN_HAND' },
                'inventory_type' : { 'type' : 'TWOHWEAPON' },
                'item_subclass' : { 'name' : 'Axe' }}]}}

    assert True == is_off_hand_weapon(profile)

def test_no_weapon_means_off_hand_is_weapon():
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Warlock' },
                'active_spec' : { 'name' : 'Destruction' }},
            'equipment' : { 'equipped_items' : []}}

    assert True == is_off_hand_weapon(profile)

def test_active_spec_is_missing():
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Warrior' }},
            'equipment' : { 'equipped_items' : [{
                'slot' : { 'type' : 'MAIN_HAND' },
                'inventory_type' : { 'type' : 'TWOHWEAPON' },
                'item_subclass' : { 'name' : 'Axe' }}]}}

    assert False == is_off_hand_weapon(profile)

@pytest.mark.parametrize("subclass", ['Bow', 'Crossbow', 'Gun'])
def test_ranged_hunter_weapons_no_offhand(subclass):
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Hunter' },
                'active_spec' : { 'name' : 'Marksmanship' }},
            'equipment' : { 'equipped_items' : [{
                'slot' : { 'type' : 'MAIN_HAND' },
                'inventory_type' : { 'type' : 'WEAPON' },
                'item_subclass' : { 'name' : subclass }}]}}

    assert False == is_off_hand_weapon(profile)

@pytest.mark.parametrize("slot", ['head', 'neck', 'shoulder', 'back',
    'chest', 'waist', 'legs', 'finger_1', 'finger_2', 'trinket_1',
    'trinket_2', 'main_hand', 'off_hand'])
def test_is_primary_enchant_not_wrist_hands_or_feet(slot):
    assert False == is_primary_enchant_slot(None, slot)

@pytest.mark.parametrize("character_class", ['Mage', 'Priest', 'Warlock'])
def test_is_primary_enchant_clothies_true_on_wrists_only(character_class):
    profile = { 'summary' : { 'character_class' : { 'name' : character_class } } }

    assert True == is_primary_enchant_slot(profile, 'wrist')
    assert False == is_primary_enchant_slot(profile, 'hands')
    assert False == is_primary_enchant_slot(profile, 'feet')

@pytest.mark.parametrize("character_class", ['Demon Hunter', 'Hunter', 'Rogue'])
def test_is_primary_enchant_agility_classes(character_class):
    profile = { 'summary' : { 'character_class' : { 'name' : character_class } } }

    assert False == is_primary_enchant_slot(profile, 'wrist')
    assert False == is_primary_enchant_slot(profile, 'hands')
    assert True == is_primary_enchant_slot(profile, 'feet')

@pytest.mark.parametrize("character_class", ['Death Knight', 'Warrior'])
def test_is_primary_enchant_strength_classes(character_class):
    profile = { 'summary' : { 'character_class' : { 'name' : character_class } } }

    assert False == is_primary_enchant_slot(profile, 'wrist')
    assert True == is_primary_enchant_slot(profile, 'hands')
    assert False == is_primary_enchant_slot(profile, 'feet')

@pytest.mark.parametrize("class_spec",
        [{'class' : 'Druid', 'spec' : 'Feral'},
         {'class' : 'Druid', 'spec' : 'Guardian'},
         {'class' : 'Monk', 'spec' : 'Brewmaster'},
         {'class' : 'Monk', 'spec' : 'Windwalker'},
         {'class' : 'Shaman', 'spec' : 'Enhancement'}])
def test_is_primary_enchant_agi_specs(class_spec):
    profile = {
            'summary' : {
                'character_class' : { 'name' : class_spec['class'] },
                'active_spec' : { 'name' : class_spec['spec'] }}}

    assert False == is_primary_enchant_slot(profile, 'wrist')
    assert False == is_primary_enchant_slot(profile, 'hands')
    assert True == is_primary_enchant_slot(profile, 'feet')

@pytest.mark.parametrize("class_spec",
        [{'class' : 'Druid', 'spec' : 'Balance'},
         {'class' : 'Druid', 'spec' : 'Restoration'},
         {'class' : 'Monk', 'spec' : 'Mistweaver'},
         {'class' : 'Shaman', 'spec' : 'Elemental'},
         {'class' : 'Shaman', 'spec' : 'Restoration'},
         {'class' : 'Paladin', 'spec' : 'Holy'}])
def test_is_primary_enchant_int_specs(class_spec):
    profile = {
            'summary' : {
                'character_class' : { 'name' : class_spec['class'] },
                'active_spec' : { 'name' : class_spec['spec'] }}}

    assert True == is_primary_enchant_slot(profile, 'wrist')
    assert False == is_primary_enchant_slot(profile, 'hands')
    assert False == is_primary_enchant_slot(profile, 'feet')

@pytest.mark.parametrize("spec", ['Protection', 'Retribution'])
def test_is_primary_enchant_strength_paladin(spec):
    profile = {
            'summary' : {
                'character_class' : { 'name' : 'Paladin' },
                'active_spec' : { 'name' : spec }}}

    assert False == is_primary_enchant_slot(profile, 'wrist')
    assert True == is_primary_enchant_slot(profile, 'hands')
    assert False == is_primary_enchant_slot(profile, 'feet')

def test_is_primary_enchant_unrecognized_is_just_false():
    profile = { 'summary' : { 'character_class' : { 'name' : "Tinkerer" } } }

    assert False == is_primary_enchant_slot(profile, 'wrist')
    assert False == is_primary_enchant_slot(profile, 'hands')
    assert False == is_primary_enchant_slot(profile, 'feet')
