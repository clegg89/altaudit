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
