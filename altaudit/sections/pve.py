"""Pull PvE Data from API"""

from ..constants import WEEKLY_EVENT_QUESTS

def pve(character, response):
    _island_expeditions(character, response)

    character.weekly_event_done = 'FALSE'
    for event_quest in WEEKLY_EVENT_QUESTS:
        if event_quest in response['quests']:
            character.weekly_event_done = 'TRUE'
            break

def _island_expeditions(character, response):
    if 53435 in response['quests'] or 53436 in response['quests']:
        character.island_weekly_done = 'TRUE'
    else:
        character.island_weekly_done = 'FALSE'

    character.islands_total = 0
    achievementCriteria = response['achievements']['criteria']
    achievementCriteriaQuantity = response['achievements']['criteriaQuantity']
    for criteria in (40563, 40564, 40565):
        if criteria in achievementCriteria:
            character.islands_total += achievementCriteriaQuantity[achievementCriteria.index(criteria)]
