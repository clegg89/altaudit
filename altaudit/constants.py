"""Charfetch Program Constants"""

RAIDERIO_URL="https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={character_name}&fields=mythic_plus_scores_by_season,mythic_plus_highest_level_runs,mythic_plus_weekly_highest_level_runs"

"""
Reset days and times.

All values are in UTC time to avoid daylight savings issues

use time.strptime(day, "%A").tm_wday to convert day string to weekday
"""
WEEKLY_RESETS = {
    'us' : { 'hour' : 15, 'day' : 'Tuesday' },
    'eu' : { 'hour' : 7, 'day' : 'Wednesday' },
    'kr' : { 'hour' : 7, 'day' : 'Wednesday' },
    'tw' : { 'hour' : 7, 'day' : 'Wednesday' }
}

"Item slots tracked"
ITEM_SLOTS = [
    'head', 'neck', 'shoulder', 'back',
    'chest', 'wrist', 'hands', 'waist',
    'legs', 'feet', 'finger1', 'finger2',
    'trinket1', 'trinket2', 'mainHand', 'offHand'
]

"Item Fields to use in Character Model"
ITEM_FIELD_COLUMNS = [
    ('itemLevel','Column(Integer)'),
    ('id', 'Column(Integer)'),
    ('name', 'Column(String)'),
    ('icon', 'Column(String)'),
    ('quality', 'Column(Integer)')]

"Item Fields"
ITEM_FIELDS = [field[0] for field in ITEM_FIELD_COLUMNS]

"Azerite piece item slots"
AZERITE_ITEM_SLOTS = [ 'head', 'shoulder', 'chest' ]

"Number of Azerite Tiers"
AZERITE_TIERS = 5

"WoW expansions"
EXPACS = [
    'classic', 'burning_crusade', 'wrath_of_the_lich_king',
    'cataclysm', 'mists_of_pandaria', 'warlords_of_draenor',
    'legion', 'battle_for_azeroth'
]

"Region to use when fetching game data"
BLIZZARD_REGION = 'us'

"Locale to use when fetching"
BLIZZARD_LOCALE = 'en_US'

"Fields to use in character profile fetch"
BLIZZARD_CHARACTER_FIELDS = [
    'items',
    'reputation',
    'audit',
    'statistics'
    'achievements',
    'professions',
    'quests'
]

"Column Headers and their database types"
CHARACTER_HEADER_FIELDS = {
    # Basic Info
    'name_api' : 'Column(String)',
    'realm_name' : "Column(Integer)",
    'realm_slug' : "association_proxy('realm', 'name')",
    'region_name' : "association_proxy('realm', 'region_name')",
    'lastmodified' : 'Column(Integer)',
    'class_name' : "association_proxy('character_class', 'name')",
    'level' : 'Column(Integer)',
    'mainspec' : 'Column(String)',
    'faction_name' : "association_proxy('faction', 'name')",
    'gender' : 'Column(String)',
    'race_name' : "association_proxy('race', 'name')",
    'avatar' : 'Column(String)',
    'bust' : 'Column(String)',
    'render' : 'Column(String)',

    # Item Info
    'estimated_ilvl' : 'Column(Float)',

    **{'{}_{}'.format(slot, item[0]) : item[1]
        for slot in ITEM_SLOTS
        for item in ITEM_FIELD_COLUMNS},

    # Azerite Info
    'hoa_level' : 'Column(Integer)',
    'azerite_experience' : 'Column(Integer)',
    'azerite_experience_remaining' : 'Column(Integer)',
    'azerite_this_week' : "''", # Obtained of snapshots

    **{'{}_tier{}_{}'.format(piece, tier, field) : "''" # Composite from azerite_traits table
        for piece in AZERITE_ITEM_SLOTS
        for tier in range(AZERITE_TIERS)
        for field in ['available', 'selected']},

    # Gear Audit
    **{'{}_enchant_{}'.format(slot, field[0]) : field[1]
        for slot in ['mainHand', 'offHand', 'finger1', 'finger2', 'hand', 'wrist']
        for field in [('id', 'Column(Integer)'), ('quality', 'Column(Integer)'), ('name', 'Column(String)'), ('description', 'Column(String)')]},

    'empty_sockets' : 'Column(Integer)',

    **{'gem_{}'.format(field) : "''" # Composite from gems table
        for field in ['ids', 'qualities', 'names', 'icons', 'stats', 'slots']},

    # Profession Info
    **{'{}_{}'.format(prof, field[0]) : field[1]
        for prof in ['primary1', 'primary2', 'cooking', 'fishing']
        for field in [('name', 'Column(String)'), ('icon', 'Column(String)'),
            *[('{}_{}'.format(expac, f), 'Column(Integer)')
                for expac in EXPACS for f in ['level', 'max']]]},

    **{'archaeology_{}'.format(field[0]) : field[1] for field in
        [('name', 'Column(String)'), ('icon', 'Column(String)'), ('level', 'Column(Integer)'), ('max', 'Column(Integer)')]},

    # Reputations
    'reputations' : 'Column(String)',

    # PvE and RaiderIO
    'island_weekly_done' : 'Column(String)',
    'islands_total' : 'Column(Integer)',
    'world_quests_total' : 'Column(Integer)',
    'world_quests_weekly' : "''", # Obtained from snapshots
    'weekly_event_done' : 'Column(String)',
    'dungeons_total' : 'Column(Integer)',
    'dungeons_each_total' : 'Column(String)',
    'dungeons_weekly' : "''", # Obtained from snapshots
    'raiderio_score' : 'Column(Float)',
    'mplus_weekly_highest' : 'Column(Integer)',
    'mplus_season_highest' : 'Column(Integer)',

    **{'raids_{}'.format(difficulty) : 'Column(String)'
        for difficulty in ['lfr', 'nromal', 'heroic', 'mythic']}
}

HEADERS = [k for k in CHARACTER_HEADER_FIELDS.keys()]
