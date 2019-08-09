"""Pull PvE Data from API"""

from ..constants import WEEKLY_EVENT_QUESTS

def pve(character, response):
    _island_expeditions(character, response)
    _world_quests(character, response)
    _weekly_event(character, response)
    _dungeons(character, response)

def _island_expeditions(character, response):
    if 53435 in response['quests'] or 53436 in response['quests']:
        character.island_weekly_done = 'TRUE'
    else:
        character.island_weekly_done = 'FALSE'

    character.islands_total = 0
    achiev_crit = response['achievements']['criteria']
    achiev_crit_quantity = response['achievements']['criteriaQuantity']
    for criteria in (40563, 40564, 40565):
        if criteria in achiev_crit:
            character.islands_total += achiev_crit_quantity[achiev_crit.index(criteria)]

def _world_quests(character, response):
    wq_criteria_index = response['achievements']['criteria'].index(33094)
    achiev_crit_quantity = response['achievements']['criteriaQuantity']
    wq_total = achiev_crit_quantity[wq_criteria_index] if wq_criteria_index in achiev_crit_quantity else 0
    character.world_quests_total = wq_total

def _weekly_event(character, response):
    character.weekly_event_done = 'FALSE'
    for event_quest in WEEKLY_EVENT_QUESTS:
        if event_quest in response['quests']:
            character.weekly_event_done = 'TRUE'
            break

def _dungeons(character, response):
