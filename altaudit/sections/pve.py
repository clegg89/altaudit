"""Pull PvE Data from API"""

from ..blizzard import BLIZZARD_LOCALE
from ..models import RAID_DIFFICULTIES
from ..utility import Utility
from .raids import VALID_RAIDS

"Quest IDs for weekly island quest"
WEEKLY_ISLAND_QUEST_IDS = (53435, 53436)

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

"Dungeons and Raids statistics category ID"
DUNGEONS_AND_RAIDS_CATEGORY_ID = 14807

"Battle for Azeroth Sub-Category ID"
BATTLE_FOR_AZEROTH_SUBCATEGORY_ID = 15409

"Mythic Dungeon Statistic IDs"
MYTHIC_DUNGEON_STATISTIC_IDS = {
    "Atal'Dazar"           : 12749,
    'Freehold'             : 12752,
    "King's Rest"          : 12763,
    'The MOTHERLODE!!'     : 12779,
    'Shrine of the Storm'  : 12768,
    'Siege of Boralus'     : 12773,
    'Temple of Sethraliss' : 12776,
    'Tol Dagor'            : 12782,
    'Underrot'             : 12745,
    'Waycrest Manor'       : 12785,
    'Operation: Mechagon'  : 13620
}

def pve(character, response, db_session, api):
    _island_expeditions(character, response)
    _world_quests(character, response)
    _weekly_event(character, response)
    _dungeons(character, response)
    # _raids(character, response)

def _island_expeditions(character, response):
    weekly_islands = next((quest for quest in response['quests_completed']['quests'] if quest['id'] in WEEKLY_ISLAND_QUEST_IDS), None)
    character.island_weekly_done = "TRUE" if weekly_islands else "FALSE"

    character.islands_total = 0
    achievements = response['achievements']['achievements']
    for achievment_id in (PVE_ISLAND_ACHIEVEMENT_ID, PVP_ISLAND_ACHIEVEMENT_ID):
        achievment = next((achiev for achiev in achievements if achiev['id'] == achievment_id), None)
        if achievment:
            character.islands_total += achievment['criteria']['child_criteria'][0]['amount']

def _world_quests(character, response):
    character.world_quests_total = next((achiev['criteria']['child_criteria'][0]['amount']
        for achiev in response['achievements']['achievements']
        if achiev['id'] == WORLD_QUESTS_COMPLETED_ACHIEVEMENT_ID), 0)

def _weekly_event(character, response):
    character.weekly_event_done = 'FALSE'
    for event_quest_id in WEEKLY_EVENT_QUESTS:
        completed_quest = next((quest for quest in response['quests_completed']['quests'] if quest['id'] == event_quest_id), None)
        if completed_quest:
            character.weekly_event_done = 'TRUE'
            break

def _dungeons(character, response):
    """
    We used to be able to get dungeon clears from achivement criteria, but that
    doesn't exist in the profile API as it did in the community API. Instead we
    have to rely on statistics (called achievement statistics in the profile API)
    to determine boss kills. This value is lower than the achievement value. It is
    unclear why, but this isn't exactly an important stat post expac release.
    """
    statistics = response['achievements_statistics']['statistics']
    # This will throw an exception if the category/subcategory is not found.
    # Is that okay? Does it matter? It shouldn't ever happen...
    # Leave it this way for now. If we start seeing errors here we can change it
    dungeon_and_raids = next(category for category in statistics if category['id'] == DUNGEONS_AND_RAIDS_CATEGORY_ID)['sub_categories']
    bfa_instances = next(sub for sub in dungeon_and_raids if sub['id'] == BATTLE_FOR_AZEROTH_SUBCATEGORY_ID)['statistics']

    dungeon_list = {dungeon : next((stat['quantity'] for stat in bfa_instances if stat['id'] == stat_id), 0)
            for dungeon,stat_id in MYTHIC_DUNGEON_STATISTIC_IDS.items()}

    character.dungeons_total = sum(dungeon_list.values())
    character.dungeons_each_total = '|'.join(('{}+{}'.format(d,a) for d,a in dungeon_list.items()))

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
