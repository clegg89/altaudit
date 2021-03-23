"""Pull PvE Data from API"""

from ..blizzard import BLIZZARD_LOCALE
from ..models import RAID_DIFFICULTIES
from ..utility import Utility
from .raids import VALID_RAIDS

"Achievement ID for 200 World Quests Completed (WQ count)"
WORLD_QUESTS_COMPLETED_ACHIEVEMENT_ID = 11127

"""
Weekly Event Quest IDs

To find these I think use:

https://www.wowhead.com/quests/world-events/weekend-event

If that fails just copy wowaudit

Use:
https://www.wowhead.com/quest={id}

To view the quest
"""
WEEKLY_EVENT_QUESTS = [
    62631, # The World Awaits (20 WQ)
    62635, # A Shrouded Path Through Time (MoP Timewalking)
    62636, # A Savage Path Through Time (WoD Timewalking)
    62637, # A Call to Battle (Win 4 BGs)
    62638, # Emissary of War (4 M0's)
    62639, # The Very Best (PvP Pet Battles)
    62640  # The Arena Calls (10 skirmishes)
]

"Dungeons and Raids statistics category ID"
DUNGEONS_AND_RAIDS_CATEGORY_ID = 14807

"Current Expac Dungeons & Raids Achievment Statistics Sub-Category ID"
CURRENT_EXPAC_SUBCATEGORY_ID = 15409

"""
Mythic Dungeon Statistic IDs

To find these values, go to Achievement Statistics Profile.
Find the Dungeons & Raids Category (ID 14807 Name Dungeons & Raids).
Find the appropriate expansion subcategory (will have that name).
Expand statistics in subcategory, and look for dungeons in each subcategory.
"""
MYTHIC_DUNGEON_STATISTIC_IDS = {
    'Halls of Atonement'    : 14392,
    'Mists of Tirna Scithe' : 14395,
    'The Necrotic Wake'     : 14404,
    'De Other Side'         : 14389,
    'Plaguefall'            : 14398,
    'Sanguine Depths'       : 14205,
    'Spires of Ascension'   : 14401,
    'Theater of Pain'      : 14407
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
            for sub in dungeon_and_raids if sub['id'] == CURRENT_EXPAC_SUBCATEGORY_ID), [])
    except (TypeError, KeyError):
        bfa_instances = []

    _world_quests(character, profile)
    _weekly_event(character, profile)
    _dungeons(character, bfa_instances)
    _raids(character, bfa_instances)

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
