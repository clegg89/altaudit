"""Pull PvE Data from API"""

from ..constants import WEEKLY_EVENT_QUESTS, MYTHIC_DUNGEONS, RAID_DIFFICULTIES, VALID_RAIDS
from ..utility import Utility

def pve(character, response):
    _island_expeditions(character, response)
    _world_quests(character, response)
    _weekly_event(character, response)
    _dungeons(character, response)
    _raids(character, response)

def _island_expeditions(character, response):
    if 53435 in response['quests'] or 53436 in response['quests']:
        character.island_weekly_done = 'TRUE'
    else:
        character.island_weekly_done = 'FALSE'

    character.islands_total = 0
    achiev_crit = response['achievements']['criteria']
    achiev_crit_quantity = response['achievements']['criteriaQuantity']
    for criteria in (40564, 40565): # PvE, PvP
        if criteria in achiev_crit:
            character.islands_total += achiev_crit_quantity[achiev_crit.index(criteria)]

def _world_quests(character, response):
    try:
        wq_criteria_index = response['achievements']['criteria'].index(33094)
        achiev_crit_quantity = response['achievements']['criteriaQuantity']
        wq_total = achiev_crit_quantity[wq_criteria_index]
        character.world_quests_total = wq_total
    except ValueError:
        character.world_quests_total = 0

def _weekly_event(character, response):
    character.weekly_event_done = 'FALSE'
    for event_quest in WEEKLY_EVENT_QUESTS:
        if event_quest in response['quests']:
            character.weekly_event_done = 'TRUE'
            break

def _dungeons(character, response):
    achiev_crit = response['achievements']['criteria']
    achiev_crit_quantity = response['achievements']['criteriaQuantity']
    instance_stats = next(stat for stat in
            next(sub for sub in response['statistics']['subCategories']
                if sub['name'] == "Dungeons & Raids")['subCategories']
            if stat['name'] == 'Battle for Azeroth')['statistics']

    dungeon_count = 0
    dungeon_list = {}
    for name,(criteria,statistic) in MYTHIC_DUNGEONS.items():
        amount = 0
        if criteria and criteria in achiev_crit:
            amount = achiev_crit_quantity[achiev_crit.index(criteria)]
        if statistic:
            stat = next((s['quantity'] for s in instance_stats if s['id'] == statistic), 0)
            amount = max(amount, stat)

        dungeon_count += amount
        dungeon_list[name] = amount

    character.dungeons_total = dungeon_count
    character.dungeons_each_total = '|'.join(('{}+{}'.format(n,a) for n,a in dungeon_list.items()))

def _raids(character, response):
    raid_list = {}
    raid_output = {'{}{}'.format(difficulty,postfix) : [] for difficulty in RAID_DIFFICULTIES for postfix in ('','_weekly')}
    instance_stats = next(stat for stat in
            next(sub for sub in response['statistics']['subCategories']
                if sub['name'] == "Dungeons & Raids")['subCategories']
            if stat['name'] == 'Battle for Azeroth')['statistics']
    encounters = [encounter['raid_ids'] for raid in VALID_RAIDS for encounter in raid['encounters']]
    boss_ids = [i for encounter in encounters for ids in encounter.values() for i in ids]

    for instance in instance_stats:
        if instance['id'] in boss_ids:
            raid_list[instance['id']] = (instance['quantity'],
                    1 if (instance['lastUpdated'] / 1000) > Utility.timestamp[character.region_name] else 0)

    for encounter in encounters:
        for difficulty,ids in encounter.items():
            raid_output[difficulty].append(max([raid_list[id][0] for id in ids if id in raid_list] + [0]))
            raid_output['{}_weekly'.format(difficulty)].append(max([raid_list[id][1] for id in ids if id in raid_list] + [0]))

    for metric,data in raid_output.items():
        setattr(character, 'raids_{}'.format(metric), '|'.join(str(d) for d in data))
