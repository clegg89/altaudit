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

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_quests_key_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'garbage' : 'More garbage' },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_quests_missing_id():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'garbage' : 53436}] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'FALSE'

def test_pve_empty_achievements():
    jack = Character('jack')
    response = { 'achievements' : None,
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : None}
    jack.world_quests_total = 30

    Section.pve(jack, response, None, None)

    assert jack.world_quests_total == 30

def test_pve_achievements_key_missing():
    jack = Character('jack')
    response = { 'achievements' : {'garbage' : 'some more garbage'},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}
    jack.world_quests_total = 30

    Section.pve(jack, response, None, None)

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

    Section.pve(jack, response, None, None)

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

    Section.pve(jack, response, None, None)

    assert jack.world_quests_total == 30

def test_world_quests_total():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'id' : 11127, 'criteria' : {'child_criteria' : [{'amount' : 20}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.world_quests_total == 20

def test_world_quests_not_present_zero():
    # Necessary since world quests are part of snapshots
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

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

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'TRUE'

def test_weekly_event_not_done():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

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

    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 84
    assert jack.dungeons_each_total == "Halls of Atonement+7|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"


@pytest.fixture
def bfa_raids():
    before_reset = int((datetime.datetime(2019, 8, 5) - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    after_reset = int((datetime.datetime(2019, 8, 7) - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    return [
        # Taloc
        {'id' : 12786, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12787, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12788, 'quantity' : 8, 'last_updated_timestamp' : before_reset},
        {'id' : 12789, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        # MOTHER
        {'id' : 12790, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12791, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12792, 'quantity' : 7, 'last_updated_timestamp' : before_reset},
        {'id' : 12793, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Fetid Devourer
        {'id' : 12794, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12795, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12796, 'quantity' : 6, 'last_updated_timestamp' : before_reset},
        {'id' : 12797, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Zek'voz
        {'id' : 12798, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12799, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12800, 'quantity' : 5, 'last_updated_timestamp' : before_reset},
        {'id' : 12801, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Vectis
        {'id' : 12802, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12803, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12804, 'quantity' : 4, 'last_updated_timestamp' : before_reset},
        {'id' : 12805, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Zul
        {'id' : 12808, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12809, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12810, 'quantity' : 3, 'last_updated_timestamp' : before_reset},
        {'id' : 12811, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Mythrax the Unraveler
        {'id' : 12813, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12814, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12815, 'quantity' : 2, 'last_updated_timestamp' : before_reset},
        {'id' : 12816, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # G'huun
        {'id' : 12817, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 12818, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12819, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 12820, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Champion of the Light
        {'id' : 13328, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13329, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13330, 'quantity' : 9, 'last_updated_timestamp' : before_reset},
        {'id' : 13331, 'quantity' : 9, 'last_updated_timestamp' : before_reset},
        # Grong
        {'id' : 13332, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13344, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13333, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13346, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13334, 'quantity' : 8, 'last_updated_timestamp' : before_reset},
        {'id' : 13347, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13336, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13348, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        # Jadefire Masters
        {'id' : 13354, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13349, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13355, 'quantity' : 2, 'last_updated_timestamp' : before_reset},
        {'id' : 13350, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13356, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13351, 'quantity' : 7, 'last_updated_timestamp' : before_reset},
        {'id' : 13357, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13353, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Opulence
        {'id' : 13358, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13359, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13361, 'quantity' : 6, 'last_updated_timestamp' : before_reset},
        {'id' : 13362, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Conclave of the Chosen
        {'id' : 13363, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13364, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13365, 'quantity' : 5, 'last_updated_timestamp' : before_reset},
        {'id' : 13366, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # King Rastakhan
        {'id' : 13367, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13368, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13369, 'quantity' : 4, 'last_updated_timestamp' : before_reset},
        {'id' : 13370, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Mekkatorque
        {'id' : 13371, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13372, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13373, 'quantity' : 3, 'last_updated_timestamp' : before_reset},
        {'id' : 13374, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Stormwall Blockade
        {'id' : 13375, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13376, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13377, 'quantity' : 2, 'last_updated_timestamp' : before_reset},
        {'id' : 13378, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Lady Jaina Proudmoore
        {'id' : 13379, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13380, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13381, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13382, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # The Restless Cabal
        {'id' : 13404, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13405, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13406, 'quantity' : 2, 'last_updated_timestamp' : before_reset},
        {'id' : 13407, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Uu'nat
        {'id' : 13408, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13411, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13412, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13413, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Abyssal Command Sivara
        {'id' : 13587, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13588, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13589, 'quantity' : 8, 'last_updated_timestamp' : after_reset},
        {'id' : 13590, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Radiance of Azshara
        {'id' : 13595, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13596, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13597, 'quantity' : 7, 'last_updated_timestamp' : after_reset},
        {'id' : 13598, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Blackwater Behemoth
        {'id' : 13591, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13592, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13593, 'quantity' : 6, 'last_updated_timestamp' : after_reset},
        {'id' : 13594, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Lady Ashvane
        {'id' : 13600, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13601, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13602, 'quantity' : 5, 'last_updated_timestamp' : after_reset},
        {'id' : 13603, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Orgozoa
        {'id' : 13604, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13605, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13606, 'quantity' : 4, 'last_updated_timestamp' : after_reset},
        {'id' : 13607, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # The Queen's Court
        {'id' : 13608, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13609, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13610, 'quantity' : 3, 'last_updated_timestamp' : after_reset},
        {'id' : 13611, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Za'qul
        {'id' : 13612, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13613, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13614, 'quantity' : 2, 'last_updated_timestamp' : after_reset},
        {'id' : 13615, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Queen Azshara
        {'id' : 13616, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 13617, 'quantity' : 1, 'last_updated_timestamp' : before_reset},
        {'id' : 13618, 'quantity' : 1, 'last_updated_timestamp' : after_reset},
        {'id' : 13619, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Wrathion
        {'id' : 14078, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14079, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14080, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14082, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Maut
        {'id' : 14089, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14091, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14093, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14094, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # The Prophet Skitra
        {'id' : 14095, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14096, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14097, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14098, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Dark Inquisitor Xanesh
        {'id' : 14101, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14102, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14104, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14105, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # The Hivemind
        {'id' : 14107, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14108, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14109, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14110, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Shad'har the Insatiable
        {'id' : 14111, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14112, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14114, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14115, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Dret'agath
        {'id' : 14117, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14118, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14119, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14120, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Vexiona
        {'id' : 14123, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14124, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14125, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14126, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Ra-den the Despoiled
        {'id' : 14127, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14128, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14129, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14130, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Il'gynoth, Corruption Reborn
        {'id' : 14207, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14208, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14210, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14211, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # Carapace of N'Zoth
        {'id' : 14131, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14132, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14133, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14134, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        # N'Zoth the Corruptor
        {'id' : 14135, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14136, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14137, 'quantity' : 0, 'last_updated_timestamp' : before_reset},
        {'id' : 14138, 'quantity' : 0, 'last_updated_timestamp' : before_reset}
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
    Section.pve(jack, response, None, None)

    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '1|1|1|1|1|1|1|1|1|1|2|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '8|7|6|5|4|3|2|1|9|8|7|6|5|4|3|2|1|2|1|8|7|6|5|4|3|2|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '1|0|0|0|0|0|0|0|9|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_expac_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : []}]}}

    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_categories_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : []}}

    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_statistics_missing():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : None}

    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_sub_categories():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

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
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

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
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_dungeons_and_raids_missing_sub_categories_stats():
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 0
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+0|The Necrotic Wake+0|De Other Side+0|Plaguefall+0|Sanguine Depths+0|Spires of Ascension+0|Theater of Pain+0"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

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
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 77
    assert jack.dungeons_each_total == "Halls of Atonement+0|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|1|1|1|1|1|1|1|1|1|2|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '8|7|6|5|4|3|2|1|9|8|7|6|5|4|3|2|1|2|1|8|7|6|5|4|3|2|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '1|0|0|0|0|0|0|0|9|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

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
    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 84
    assert jack.dungeons_each_total == "Halls of Atonement+7|Mists of Tirna Scithe+8|The Necrotic Wake+9|De Other Side+10|Plaguefall+11|Sanguine Depths+12|Spires of Ascension+13|Theater of Pain+14"
    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '0|1|1|1|1|1|1|1|1|1|2|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '8|7|6|5|4|3|2|1|9|8|7|6|5|4|3|2|1|2|1|8|7|6|5|4|3|2|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '1|0|0|0|0|0|0|0|9|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'

def test_raids_missing_last_updated_timestamp(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    bad_bfa_raids = copy.deepcopy(bfa_raids)
    entry_to_alter = next(entry for entry in bad_bfa_raids if entry['id'] == 13589)
    del entry_to_alter['last_updated_timestamp']
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'categories' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : bad_bfa_raids}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None, None)

    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '1|1|1|1|1|1|1|1|1|1|2|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '8|7|6|5|4|3|2|1|9|8|7|6|5|4|3|2|1|2|1|0|7|6|5|4|3|2|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic == '1|0|0|0|0|0|0|0|9|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
