"""Pull PvE Data from API"""

from ..blizzard import BLIZZARD_LOCALE
from ..models import RAID_DIFFICULTIES
from ..utility import Utility
from .raids import VALID_RAIDS

"Achievement ID for No Tourist (Normal or higher islands)"
PVE_ISLAND_ACHIEVEMENT_ID = 12596

"Achievement ID for Bayside Brawler (PVP islands)"
PVP_ISLAND_ACHIEVEMENT_ID = 12597

"Achievement ID for 200 World Quests Completed (WQ count)"
WORLD_QUESTS_COMPLETED_ACHIEVEMENT_ID = 11127

"Weekly Event Quest IDs"
WEEKLY_EVENT_QUESTS = [
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
]

"Mythic Dungeon Information"
MYTHIC_DUNGEONS = {
    "Atal'Dazar"           : (40808, 12749),
    'Freehold'             : (40812, 12752),
    "King's Rest"          : (40959, 12763),
    'The MOTHERLODE!!'     : (40955, 12779),
    'Shrine of the Storm'  : (40941, 12768),
    'Siege of Boralus'     : (43355, 12773),
    'Temple of Sethraliss' : (40191, 12776),
    'Tol Dagor'            : (40944, 12782),
    'Underrot'             : (40184, 12745),
    'Waycrest Manor'       : (40144, 12785),
    'Operation: Mechagon'  : (None, 13620)
}

def pve(character, response, db_session, api):
    _island_expeditions(character, response)
    _world_quests(character, response)
    # _weekly_event(character, response)
    # _dungeons(character, response)
    # _raids(character, response)

def _island_expeditions(character, response):
    weekly_islands = next((quest for quest in response['quests_completed']['quests'] if quest['id'] == 53435 or quest['id'] == 53436), None)
    character.island_weekly_done = "TRUE" if weekly_islands else "FALSE"
    # if 53435 in response['quests'] or 53436 in response['quests']:
    #     character.island_weekly_done = 'TRUE'
    # else:
    #     character.island_weekly_done = 'FALSE'

    character.islands_total = 0
    achievements = response['achievements']['achievements']
    for achievment_id in (PVE_ISLAND_ACHIEVEMENT_ID, PVP_ISLAND_ACHIEVEMENT_ID):
        achievment = next((achiev for achiev in achievements if achiev['id'] == achievment_id), None)
        if achievment:
            character.islands_total += achievment['criteria']['child_criteria'][0]['amount']

def _world_quests(character, response):
    wq_total = next((achiev for achiev in response['achievements']['achievements']
        if achiev['id'] == WORLD_QUESTS_COMPLETED_ACHIEVEMENT_ID), None)
    character.world_quests_total = wq_total['criteria']['child_criteria'][0]['amount'] if wq_total else 0

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
