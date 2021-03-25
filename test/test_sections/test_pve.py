"""Unit Tests for the PvE Data"""
import pytest

import datetime
import copy

from altaudit.models import Region, Realm, Character
from altaudit.utility import Utility

import altaudit.sections.pve as Section

def test_pve_quests_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : None,
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_quests_key_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'garbage' : 'More garbage' },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_quests_missing_id():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'garbage' : 53436}] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_empty_achievements():
    jack = Character('jack')
    response = { 'achievements' : None,
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : None}
    jack.world_quests_total = 30

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 30

def test_pve_achievements_key_missing():
    jack = Character('jack')
    response = { 'achievements' : {'garbage' : 'some more garbage'},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}
    jack.world_quests_total = 30

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 30

def test_pve_achievements_missing_id():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'criteria' : {'child_criteria' : [{'amount' : 10}]}},
                {'id' : 12597, 'criteria' : {'child_criteria' : [{'amount' : 30}]}},
                {'criteria' : {'child_criteria' : [{'amount' : 40}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}
    jack.world_quests_total = 30

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 30

def test_pve_achievements_missing_id_old_value_greater_than_new():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'criteria' : {'child_criteria' : [{'amount' : 10}]}},
                {'id' : 12597, 'criteria' : {'child_criteria' : [{'amount' : 30}]}},
                {'criteria' : {'child_criteria' : [{'amount' : 40}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}
    jack.world_quests_total = 30

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 30

def test_world_quests_total():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'id' : 11127, 'criteria' : {'child_criteria' : [{'amount' : 20}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 20

def test_world_quests_not_present_zero():
    # Necessary since world quests are part of snapshots
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.world_quests_total == 0

@pytest.mark.parametrize('event_id', [
    62631, # The World Awaits (20 WQ)
    62635, # A Shrouded Path Through Time (MoP Timewalking)
    62636, # A Savage Path Through Time (WoD Timewalking)
    62637, # A Call to Battle (Win 4 BGs)
    62638, # Emissary of War (4 M0's)
    62639, # The Very Best (PvP Pet Battles)
    62640  # The Arena Calls (10 skirmishes)
    ])
def test_weekly_event_done(event_id):
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'id' : event_id}] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.weekly_event_done == 'TRUE'

def test_weekly_event_not_done():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None)

    assert jack.weekly_event_done == 'FALSE'

def test_dungeons():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : [
                        {'id' : 14392, 'quantity' : 7},
                        {'id' : 14395, 'quantity' : 8},
                        {'id' : 14404, 'quantity' : 9},
                        {'id' : 14389, 'quantity' : 10},
                        {'id' : 14398, 'quantity' : 11},
                        {'id' : 14205, 'quantity' : 12},
                        {'id' : 14401, 'quantity' : 13},
                        {'id' : 14407, 'quantity' : 14}]}]}]}}

    Section.pve(jack, response, None)

    assert jack.dungeons_total == 84
    assert jack.dungeons_each_total == "Halls of Atonement+7|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"


@pytest.fixture
def bfa_raids():
    before_reset = int((datetime.datetime(2019, 8, 5) - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    after_reset = int((datetime.datetime(2019, 8, 7) - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    return [
        # Shriekwing
        {'id' : 14422, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14419, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14420, 'quantity' : 8, 'last_updated_timestamp' : before_reset},
        {'id' : 14421, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        # Huntsman Altimor
        {'id' : 14426, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14423, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14424, 'quantity' : 7, 'last_updated_timestamp' : before_reset},
        {'id' : 14425, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Hungering Destroyer
        {'id' : 14430, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14427, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14428, 'quantity' : 6, 'last_updated_timestamp' : before_reset},
        {'id' : 14429, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Sun King's Salvation
        {'id' : 14438, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14435, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14436, 'quantity' : 5, 'last_updated_timestamp' : before_reset},
        {'id' : 14437, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Artificer Xy'mox
        {'id' : 14434, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14431, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14432, 'quantity' : 4, 'last_updated_timestamp' : before_reset},
        {'id' : 14433, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Lady Inerva Darkvein
        {'id' : 14442, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14439, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14440, 'quantity' : 3, 'last_updated_timestamp' : before_reset},
        {'id' : 14441, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # The Council of Blood
        {'id' : 14446, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14443, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14444, 'quantity' : 2, 'last_updated_timestamp' : before_reset},
        {'id' : 14445, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Sludgefist
        {'id' : 14450, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14447, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14448, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14449, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Stone Legion Generals
        {'id' : 14454, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14451, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14452, 'quantity' : 9, 'last_updated_timestamp' : before_reset},
        {'id' : 14453, 'quantity' : 9, 'last_updated_timestamp' : before_reset},
        # Sire Denathrius
        {'id' : 14458, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14455, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 14456, 'quantity' : 8, 'last_updated_timestamp' : before_reset},
        {'id' : 14457, 'quantity' : 1, 'last_updated_timestamp' : before_reset}
    ]

def test_raids_all_boss_difficulties(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : bfa_raids}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '1|1|1|1|1|1|1|1|1|1'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '8|7|6|5|4|3|2|1|9|8'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '1|0|0|0|0|0|0|0|9|1'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_expac_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : []}]}}

    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_categories_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : []}}

    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_statistics_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : None}

    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_sub_categories():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_categories_id(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'sub_categories' : [
                    {'id' : 15409, 'statistics' : [
                        {'id' : 12749, 'quantity' : 4},
                        {'id' : 12752, 'quantity' : 5},
                        {'id' : 12763, 'quantity' : 6},
                        {'id' : 12779, 'quantity' : 7},
                        {'id' : 12768, 'quantity' : 8},
                        {'id' : 12773, 'quantity' : 9},
                        {'id' : 12776, 'quantity' : 10},
                        {'id' : 12782, 'quantity' : 11},
                        {'id' : 12745, 'quantity' : 12},
                        {'id' : 12785, 'quantity' : 13},
                        {'id' : 13620, 'quantity' : 14},
                        *bfa_raids]}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_sub_categories_id(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'statistics' : [
                        {'id' : 12749, 'quantity' : 4},
                        {'id' : 12752, 'quantity' : 5},
                        {'id' : 12763, 'quantity' : 6},
                        {'id' : 12779, 'quantity' : 7},
                        {'id' : 12768, 'quantity' : 8},
                        {'id' : 12773, 'quantity' : 9},
                        {'id' : 12776, 'quantity' : 10},
                        {'id' : 12782, 'quantity' : 11},
                        {'id' : 12745, 'quantity' : 12},
                        {'id' : 12785, 'quantity' : 13},
                        {'id' : 13620, 'quantity' : 14},
                        *bfa_raids]}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_sub_categories_stats():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_stat_id(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    bad_bfa_raids = copy.deepcopy(bfa_raids)
    del bad_bfa_raids[1]['id']
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : [
                        {'quantity' : 4},
                        {'id' : 14395, 'quantity' : 8},
                        {'id' : 14404, 'quantity' : 9},
                        {'id' : 14389, 'quantity' : 10},
                        {'id' : 14398, 'quantity' : 11},
                        {'id' : 14205, 'quantity' : 12},
                        {'id' : 14401, 'quantity' : 13},
                        {'id' : 14407, 'quantity' : 14},
                        *bad_bfa_raids]}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 77
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|1|1|1|1|1|1|1|1|1'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '8|7|6|5|4|3|2|1|9|8'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '1|0|0|0|0|0|0|0|9|1'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_stat_quantity(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    bad_bfa_raids = copy.deepcopy(bfa_raids)
    del bad_bfa_raids[1]['quantity']
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : [
                        {'id' : 14392},
                        {'id' : 14395, 'quantity' : 8},
                        {'id' : 14404, 'quantity' : 9},
                        {'id' : 14389, 'quantity' : 10},
                        {'id' : 14398, 'quantity' : 11},
                        {'id' : 14205, 'quantity' : 12},
                        {'id' : 14401, 'quantity' : 13},
                        {'id' : 14407, 'quantity' : 14},
                        *bad_bfa_raids]}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.dungeons_total == 77
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"
    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '0|1|1|1|1|1|1|1|1|1'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '8|7|6|5|4|3|2|1|9|8'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '1|0|0|0|0|0|0|0|9|1'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'

def test_raids_missing_last_updated_timestamp(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    bad_bfa_raids = copy.deepcopy(bfa_raids)
    entry_to_alter = next(entry for entry in bad_bfa_raids if entry['id'] == 14432)
    del entry_to_alter['last_updated_timestamp']
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : bad_bfa_raids}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None)

    assert jack.raids_raid_finder        == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal             == '1|1|1|1|1|1|1|1|1|1'
    assert jack.raids_normal_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic             == '8|7|6|5|0|3|2|1|9|8'
    assert jack.raids_heroic_weekly      == '0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic             == '1|0|0|0|0|0|0|0|9|1'
    assert jack.raids_mythic_weekly      == '0|0|0|0|0|0|0|0|0|0'
