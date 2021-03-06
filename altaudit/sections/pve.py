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

def pve(character, profile, db_session, api):
    # This will throw an exception if the category/subcategory is not found.
    # Is that okay? Does it matter? It shouldn't ever happen...
    # Leave it this way for now. If we start seeing errors here we can change it
    try:
        statistics = profile['achievements_statistics']['categories']
        dungeon_and_raids = next((category['sub_categories']
            for category in statistics if category['id'] == DUNGEONS_AND_RAIDS_CATEGORY_ID), [])
        bfa_instances = next((sub['statistics']
            for sub in dungeon_and_raids if sub['id'] == BATTLE_FOR_AZEROTH_SUBCATEGORY_ID), [])
    except (TypeError, KeyError):
        bfa_instances = []

    _island_expeditions(character, profile)
    _world_quests(character, profile)
    _weekly_event(character, profile)
    _dungeons(character, bfa_instances)
    _raids(character, bfa_instances)

def _island_expeditions(character, profile):
    try:
        weekly_islands = next((quest for quest in profile['quests_completed']['quests']
            if quest['id'] in WEEKLY_ISLAND_QUEST_IDS), None)
        character.island_weekly_done = "TRUE" if weekly_islands else "FALSE"
    except (TypeError, KeyError):
        character.island_weekly_done = "FALSE"

    if profile['achievements'] and 'achievements' in profile['achievements']:
        new_total = 0
        achievements = profile['achievements']['achievements']
        for achievement_id in (PVE_ISLAND_ACHIEVEMENT_ID, PVP_ISLAND_ACHIEVEMENT_ID):
            achievement = next((achiev for achiev in achievements if 'id' in achiev and achiev['id'] == achievement_id), None)
            if achievement:
                try:
                    new_total += achievement['criteria']['child_criteria'][0]['amount']
                except (TypeError, KeyError):
                    pass

        character.islands_total = max(new_total, character.islands_total) if character.islands_total else new_total

def _world_quests(character, profile):
    if not character.world_quests_total:
        character.world_quests_total = 0

    if profile['achievements'] and 'achievements' in profile['achievements']:
        achievement = next((achiev for achiev in profile['achievements']['achievements']
            if 'id' in achiev and achiev['id'] == WORLD_QUESTS_COMPLETED_ACHIEVEMENT_ID), None)

        if achievement:
            try:
                character.world_quests_total = achievement['criteria']['child_criteria'][0]['amount']
            except (TypeError, KeyError):
                pass

def _weekly_event(character, profile):
    character.weekly_event_done = 'FALSE'
    try:
        for event_quest_id in WEEKLY_EVENT_QUESTS:
            completed_quest = next((quest for quest in profile['quests_completed']['quests']
                if quest['id'] == event_quest_id), None)
            if completed_quest:
                character.weekly_event_done = 'TRUE'
                break
    except (TypeError, KeyError):
        pass

def _dungeons(character, bfa_instance_stats):
    """
    We used to be able to get dungeon clears from achivement criteria, but that
    doesn't exist in the profile API as it did in the community API. Instead we
    have to rely on statistics (called achievement statistics in the profile API)
    to determine boss kills. This value is lower than the achievement value. It is
    unclear why, but this isn't exactly an important stat post expac release.
    """
    dungeon_list = {dungeon : next((int(stat['quantity'])
        for stat in bfa_instance_stats
        if 'id' in stat and
        'quantity' in stat and
        stat['id'] == stat_id), 0)
            for dungeon,stat_id in MYTHIC_DUNGEON_STATISTIC_IDS.items()}

    character.dungeons_total = sum(dungeon_list.values())
    character.dungeons_each_total = '|'.join(('{}+{}'.format(d,a) for d,a in dungeon_list.items()))

def _raids(character, bfa_instance_stats):
    raid_list = {}
    # Becomes a dictionary of format raid : [], raid_weekly : []
    raid_output = {'{}{}'.format(difficulty,postfix) : [] for difficulty in RAID_DIFFICULTIES for postfix in ('','_weekly')}
    # A list of all encounters of the form [{'raid_finder' : [ids], 'normal' : [ids], ...}, ...]
    # Some bosses (Battle of Dazar'alor) have 2 different IDs. So we get the sum of all IDs
    encounters = [encounter['raid_ids'] for raid in VALID_RAIDS for encounter in raid['encounters']]
    # The stat IDs of every raid boss
    boss_ids = [ID for encounter in encounters for ids in encounter.values() for ID in ids]

    for boss_id in boss_ids:
        # Tuple of (total, weekly), (0,0) if not found
        raid_list[boss_id] = next((
            (int(stat['quantity']),
                # Can only kill a boss 1/week, so set if the stat was updated in the last week
                1 if (stat['last_updated_timestamp']/1000) > Utility.timestamp[character.region_name] else 0)
            # Loop through all stats in bfa kills, if ID matches, get our tuple. If nothing found (0,0)
            for stat in bfa_instance_stats
            if 'id' in stat and
            'quantity' in stat and
            'last_updated_timestamp' in stat and
            stat['id'] == boss_id), (0,0))

    for encounter in encounters:
        # encounter is of the form {'difficulty' : [ids],...}
        for difficulty,ids in encounter.items():
            # If a boss has more than 1 ID, take the sum of both. List shouldn't be empty, we put (0,0) in items not found
            raid_output[difficulty].append(sum([raid_list[ID][0] for ID in ids if ID in raid_list]))
            raid_output['{}_weekly'.format(difficulty)].append(sum([raid_list[ID][1] for ID in ids if ID in raid_list]))

    # Place into character fields 'raids_{difficult}[_weekly]'
    for metric,data in raid_output.items():
        setattr(character, 'raids_{}'.format(metric), '|'.join(str(d) for d in data))
