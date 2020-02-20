"""Unit Tests for the PvE Data"""
import pytest

import datetime

from altaudit.models import Region, Realm, Character
from altaudit.utility import Utility

import altaudit.sections as Section

def test_islands_weekly_quest_done():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'id' : 53435}] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.island_weekly_done == 'TRUE'

def test_islands_weekly_quest_done_other_id():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'id' : 53436}] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.island_weekly_done == 'TRUE'

def test_islands_weekly_quest_not_done():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.island_weekly_done == 'FALSE'

def test_islands_total_sum_of_two_criteria():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'id' : 12596, 'criteria' : {'child_criteria' : [{'amount' : 10}]}},
                {'id' : 12597, 'criteria' : {'child_criteria' : [{'amount' : 30}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.islands_total == 40

def test_world_quests_total():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [
                {'id' : 11127, 'criteria' : {'child_criteria' : [{'amount' : 20}]}}]},
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.world_quests_total == 20

def test_world_quests_not_present_zero():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.world_quests_total == 0

@pytest.mark.parametrize('event_id', [
      53032, # Burning Crusade timewalking
      53036, # 4 Battleground matches
      53033, # Lich King timewalking
      53034, # Cataclysm timewalking
      53035, # Pandaria timewalking
      53037, # Emissary of war
      53039, # Arena calls
      53038, # Pet battles
      53030, # World quests
      54995, # Draenor timewalking
    ])
def test_weekly_event_done(event_id):
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [{'id' : event_id}] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'TRUE'

def test_weekly_event_not_done():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [ {'id' : 14807, 'sub_categories' : [ {'id' : 15409, 'statistics' : []}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.weekly_event_done == 'FALSE'

def test_dungeons_statistics_only():
    jack = Character('jack')
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [
                {'id' : 14807, 'sub_categories' : [
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
                        {'id' : 13620, 'quantity' : 14}]}]}]}}

    Section.pve(jack, response, None, None)

    assert jack.dungeons_total == 99
    assert jack.dungeons_each_total == "Atal'Dazar+4|Freehold+5|King's Rest+6|The MOTHERLODE!!+7|Shrine of the Storm+8|Siege of Boralus+9|Temple of Sethraliss+10|Tol Dagor+11|Underrot+12|Waycrest Manor+13|Operation: Mechagon+14"


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
    ]

def test_raids_all_boss_difficulties(bfa_raids):
    jack = Character('jack', realm=Realm('kiljaeden', Region('us')))
    now = datetime.datetime(2019, 8, 8)
    response = { 'achievements' : { 'achievements' : [] },
            'quests_completed' : { 'quests' : [] },
            'achievements_statistics' : { 'statistics' : [
                {'id' : 14807, 'sub_categories' : [
                    {'id' : 15409, 'statistics' : bfa_raids}]}]}}

    Utility.set_refresh_timestamp(now)
    Section.pve(jack, response, None, None)

    assert jack.raids_raid_finder == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_raid_finder_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_normal == '1|1|1|1|1|1|1|1|1|1|2|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1'
    assert jack.raids_normal_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_heroic == '8|7|6|5|4|3|2|1|9|8|7|6|5|4|3|2|1|2|1|8|7|6|5|4|3|2|1'
    assert jack.raids_heroic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|1|1|1|1|1|1|1'
    assert jack.raids_mythic == '1|0|0|0|0|0|0|0|9|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
    assert jack.raids_mythic_weekly == '0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0'
