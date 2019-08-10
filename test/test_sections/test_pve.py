"""Unit Tests for the PvE Data"""
import pytest

from altaudit.models import Character

import altaudit.sections as Section

def test_islands_weekly_quest_done():
    jack = Character('jack')
    response = {
            'quests' : [53435],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.island_weekly_done == 'TRUE'

def test_islands_weekly_quest_done_other_id():
    jack = Character('jack')
    response = {
            'quests' : [53436],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.island_weekly_done == 'TRUE'

def test_islands_weekly_quest_not_done():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [33094],
                'criteriaQuantity' : [0]},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.island_weekly_done == 'FALSE'

def test_islands_total_sum_of_three_criteria():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [40563, 40564, 40565],
                'criteriaQuantity' : [4, 10, 30]},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.islands_total == 44

def test_world_quests_total():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [33094],
                'criteriaQuantity' : [20]},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.world_quests_total == 20

def test_world_quests_not_present_zero():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

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
    response = {
            'quests' : [event_id],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.weekly_event_done == 'TRUE'

def test_weekly_event_not_done():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.weekly_event_done == 'FALSE'

def test_dungeons_achievement_only():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [40808, 40812, 40959, 40955, 40941, 43355, 40191, 40944, 40184, 40144],
                'criteriaQuantity' : [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : []}]}]}}

    Section.pve(jack, response)

    assert jack.dungeons_total == 85
    assert jack.dungeons_each_total == "Atal'Dazar+4|Freehold+5|King's Rest+6|The MOTHERLODE!!+7|Shrine of the Storm+8|Siege of Boralus+9|Temple of Sethraliss+10|Tol Dagor+11|Underrot+12|Waycrest Manor+13|Operation: Mechagon+0"

def test_dungeons_statistics_only():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [],
                'criteriaQuantity' : []},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : [
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

    Section.pve(jack, response)

    assert jack.dungeons_total == 99
    assert jack.dungeons_each_total == "Atal'Dazar+4|Freehold+5|King's Rest+6|The MOTHERLODE!!+7|Shrine of the Storm+8|Siege of Boralus+9|Temple of Sethraliss+10|Tol Dagor+11|Underrot+12|Waycrest Manor+13|Operation: Mechagon+14"

def test_dungeons_take_greater():
    jack = Character('jack')
    response = {
            'quests' : [],
            'achievements' : {
                'criteria' : [40808, 40812, 40959, 40955, 40941, 43355, 40191, 40944, 40184, 40144],
                'criteriaQuantity' : [4, 3, 6, 7, 8, 9, 1, 11, 12, 13]},
            'statistics' : {
                'subCategories' : [
                    {'name' : 'Dungeons & Raids', 'subCategories' : [
                        {'name' : 'Battle for Azeroth', 'statistics' : [
                            {'id' : 12749, 'quantity' : 4},
                            {'id' : 12752, 'quantity' : 5},
                            {'id' : 12763, 'quantity' : 2},
                            {'id' : 12779, 'quantity' : 7},
                            {'id' : 12768, 'quantity' : 8},
                            {'id' : 12773, 'quantity' : 9},
                            {'id' : 12776, 'quantity' : 10},
                            {'id' : 12782, 'quantity' : 0},
                            {'id' : 12745, 'quantity' : 1},
                            {'id' : 12785, 'quantity' : 13},
                            {'id' : 13620, 'quantity' : 14}]}]}]}}

    Section.pve(jack, response)

    assert jack.dungeons_total == 99
    assert jack.dungeons_each_total == "Atal'Dazar+4|Freehold+5|King's Rest+6|The MOTHERLODE!!+7|Shrine of the Storm+8|Siege of Boralus+9|Temple of Sethraliss+10|Tol Dagor+11|Underrot+12|Waycrest Manor+13|Operation: Mechagon+14"
