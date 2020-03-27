"""Unit Tests for the sections utilities"""
import pytest

from altaudit.sections.utility import is_off_hand_weapon

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
