"""Charfetch Program Constants"""

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

"Item slots that can be enchanted (for BfA)"
ENCHANTED_ITEM_SLOTS = [ 'mainHand', 'offHand', 'finger1', 'finger2', 'hand', 'wrist' ]

"Item Enchant filds for use in Character Model"
ENCHANT_ITEM_FIELD_COLUMNS = [
        ('id', 'Column(Integer)'),
        ('quality', 'Column(Integer)'),
        ('name', 'Column(String)'),
        ('description', 'Column(String)')]

"Item Enchant Fields"
ENCHANT_ITEM_FIELDS = [field[0] for field in ENCHANT_ITEM_FIELD_COLUMNS]

"Professions, excluding Archaeology"
PROFESSIONS = ['primary1', 'primary2', 'cooking', 'fishing']

"List of all expacs and their profession prefix"
PROFESSION_EXPACS = {
    '' : 'classic',
    'Outland' : 'burning_crusade',
    'Northrend' : 'wrath_of_the_lich_king',
    'Cataclysm' : 'cataclysm',
    'Pandaria' : 'mists_of_pandaria',
    'Draenor' : 'warlords_of_draenor',
    'Legion' : 'legion',
    'Kul Tiran' : 'battle_for_azeroth'}

"WoW expansions"
EXPACS = [v for v in PROFESSION_EXPACS.values()]

"Profession Field Columns excluding Archaeology"
PROFESSION_FIELD_COLUMNS = [
    ('name', 'Column(String)'),
    ('icon', 'Column(String)'),
    *[('{}_{}'.format(expac, f), 'Column(Integer)')
        for expac in EXPACS for f in ['level', 'max']]]

"Profession Fields"
PROFESSION_FIELDS = [f[0] for f in PROFESSION_FIELD_COLUMNS]

"Archaeology Field Columns"
ARCHAEOLOGY_FIELD_COLUMNS = [
    ('name', 'Column(String)'),
    ('icon', 'Column(String)'),
    ('level', 'Column(Integer)'),
    ('max', 'Column(Integer)')]

"Archaeology Fields"
ARCHAEOLOGY_FIELDS = [f[0] for f in ARCHAEOLOGY_FIELD_COLUMNS]

"Faction IDs for Reputations"
REPUTATION_FACTION_ID = {
    'alliance' : [
        2160, # Proudbmoore Admiralty
        2162, # Storm's Wake
        2161, # Order of Embers
        2159, # 7th Legion
        2164, # Champions of Azeroth
        2163, # Tortollan Seekers
        2400, # Waveblade Ankoan
        2391  # Rustbolt Resistance
    ],
    'horde' : [
        2103, # Zandalari Empire
        2156, # Talanji's Expedition
        2158, # Voldunai
        2157, # The Honorbound
        2164, # Champions of Azeroth
        2163, # Tortollan Seekers
        2373, # The Unshackled
        2391  # Rustbolt Resistance
    ]
}

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

"Raid Difficulties"
RAID_DIFFICULTIES = [
    'raid_finder', 'normal', 'heroic', 'mythic'
]

"""
Raid Information

Note that raid id is the WCL zone, and the encounter id is the WCL encounter. We use Neither
"""
VALID_RAIDS = [{
  'name' : 'Uldir', 'id' : 19,
  'encounters' : [{
    'id' : 2144, 'name' : 'Taloc', 'raid_ids' : {
      'raid_finder' : [12786], 'normal' : [12787], 'heroic' : [12788], 'mythic' : [12789]
    }
  }, {
    'id' : 2141, 'name' : 'MOTHER', 'raid_ids' : {
      'raid_finder' : [12790], 'normal' : [12791], 'heroic' : [12792], 'mythic' : [12793]
    }
  }, {
    'id' : 2128, 'name' : 'Fetid Devourer', 'raid_ids' : {
      'raid_finder' : [12794], 'normal' : [12795], 'heroic' : [12796], 'mythic' : [12797]
    }
  }, {
    'id' : 2136, 'name' : "Zek'voz, Herald of N'zoth", 'raid_ids' : {
      'raid_finder' : [12798], 'normal' : [12799], 'heroic' : [12800], 'mythic' : [12801]
    }
  }, {
    'id' : 2134, 'name' : 'Vectis', 'raid_ids' : {
      'raid_finder' : [12802], 'normal' : [12803], 'heroic' : [12804], 'mythic' : [12805]
    }
  }, {
    'id' : 2145, 'name' : 'Zul, Reborn', 'raid_ids' : {
      'raid_finder' : [12808], 'normal' : [12809], 'heroic' : [12810], 'mythic' : [12811]
    }
  }, {
    'id' : 2135, 'name' : 'Mythrax the Unraveler', 'raid_ids' : {
      'raid_finder' : [12813], 'normal' : [12814], 'heroic' : [12815], 'mythic' : [12816]
    }
  }, {
    'id' : 2122, 'name' : "G'huun", 'raid_ids' : {
      'raid_finder' : [12817], 'normal' : [12818], 'heroic' : [12819], 'mythic' : [12820]
    }
  }]
}, {
  'name' : "Battle of Dazar'alor", 'id' : 21,
  'encounters' : [{
    'id' : 2265, 'name' : 'Champion of the Light', 'raid_ids' : {
      'raid_finder' : [13328], 'normal' : [13329], 'heroic' : [13330], 'mythic' : [13331]
    }
  }, {
    'id' : 2263, 'name' : 'Grong', 'raid_ids' : {
      'raid_finder' : [13332, 13344], 'normal' : [13333, 13346], 'heroic' : [13334, 13347], 'mythic' : [13336, 13348]
    }
  }, {
    'id' : 2266, 'name' : 'Jadefire Masters', 'raid_ids' : {
      'raid_finder' : [13354, 13349], 'normal' : [13355, 13350], 'heroic' : [13356, 13351], 'mythic' : [13357, 13353]
    }
  }, {
    'id' : 2271, 'name' : 'Opulence', 'raid_ids' : {
      'raid_finder' : [13358], 'normal' : [13359], 'heroic' : [13361], 'mythic' : [13362]
    }
  }, {
    'id' : 2268, 'name' : 'Conclave of the Chosen', 'raid_ids' : {
      'raid_finder' : [13363], 'normal' : [13364], 'heroic' : [13365], 'mythic' : [13366]
    }
  }, {
    'id' : 2272, 'name' : 'King Rastakhan', 'raid_ids' : {
      'raid_finder' : [13367], 'normal' : [13368], 'heroic' : [13369], 'mythic' : [13370]
    }
  }, {
    'id' : 2276, 'name' : 'Mekkatorque', 'raid_ids' : {
      'raid_finder' : [13371], 'normal' : [13372], 'heroic' : [13373], 'mythic' : [13374]
    }
  }, {
    'id' : 2280, 'name' : 'Stormwall Blockade', 'raid_ids' : {
      'raid_finder' : [13375], 'normal' : [13376], 'heroic' : [13377], 'mythic' : [13378]
    }
  }, {
    'id' : 2281, 'name' : 'Lady Jaina Proudmoore', 'raid_ids' : {
      'raid_finder' : [13379], 'normal' : [13380], 'heroic' : [13381], 'mythic' : [13382]
    }
  }]
}, {
  'name' : 'Crucible of Storms', 'id' : 22,
  'encounters' : [{
    'id' : 2269, 'name' : 'The Restless Cabal', 'raid_ids' : {
      'raid_finder' : [13404], 'normal' : [13405], 'heroic' : [13406], 'mythic' : [13407]
    }
  }, {
    'id' : 2273, 'name' : "Uu'nat, Harbinger of the Void", 'raid_ids' : {
      'raid_finder' : [13408], 'normal' : [13411], 'heroic' : [13412], 'mythic' : [13413]
    }
  }]
}, {
  'name' : 'The Eternal Palace', 'id' : 23,
  'encounters' : [{
    'id' : 2298, 'name' : 'Abyssal Commander Sivara', 'raid_ids' : {
      'raid_finder' : [13587], 'normal' : [13588], 'heroic' : [13589], 'mythic' : [13590]
    }
  }, {
    'id' : 2305, 'name' : "Radiance of Azshara", 'raid_ids' : {
      'raid_finder' : [13595], 'normal' : [13596], 'heroic' : [13597], 'mythic' : [13598]
    }
  }, {
    'id' : 2289, 'name' : "Blackwater Behemoth", 'raid_ids' : {
      'raid_finder' : [13591], 'normal' : [13592], 'heroic' : [13593], 'mythic' : [13594]
    }
  }, {
    'id' : 2304, 'name' : "Lady Ashvane", 'raid_ids' : {
      'raid_finder' : [13600], 'normal' : [13601], 'heroic' : [13602], 'mythic' : [13603]
    }
  }, {
    'id' : 2303, 'name' : "Orgozoa", 'raid_ids' : {
      'raid_finder' : [13604], 'normal' : [13605], 'heroic' : [13606], 'mythic' : [13607]
    }
  }, {
    'id' : 2311, 'name' : "The Queen's Court", 'raid_ids' : {
      'raid_finder' : [13608], 'normal' : [13609], 'heroic' : [13610], 'mythic' : [13611]
    }
  }, {
    'id' : 2293, 'name' : "Za'qul", 'raid_ids' : {
      'raid_finder' : [13612], 'normal' : [13613], 'heroic' : [13614], 'mythic' : [13615]
    }
  }, {
    'id' : 2299, 'name' : "Queen Azshara", 'raid_ids' : {
      'raid_finder' : [13616], 'normal' : [13617], 'heroic' : [13618], 'mythic' : [13619]
    }
  }]
}]

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

    **{'{}_tier{}_{}'.format(piece, tier, field) : "''" # Composite from azerite_traits table
        for piece in AZERITE_ITEM_SLOTS
        for tier in range(AZERITE_TIERS)
        for field in ['available', 'selected']},

    # Gear Audit
    **{'{}_enchant_{}'.format(slot, field[0]) : field[1]
        for slot in ENCHANTED_ITEM_SLOTS
        for field in ENCHANT_ITEM_FIELD_COLUMNS},

    'empty_sockets' : 'Column(Integer)',

    **{'gem_{}'.format(field) : "''" # Composite from gems table
        for field in ['ids', 'qualities', 'names', 'icons', 'stats', 'slots']},

    # Profession Info
    **{'{}_{}'.format(prof, field[0]) : field[1]
        for prof in PROFESSIONS
        for field in PROFESSION_FIELD_COLUMNS},

    **{'archaeology_{}'.format(field[0]) : field[1] for field in
        ARCHAEOLOGY_FIELD_COLUMNS},

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
        for difficulty in RAID_DIFFICULTIES},

    **{'raids_{}_weekly'.format(difficulty) : 'Column(String)'
        for difficulty in RAID_DIFFICULTIES}
}

HEADERS = [k for k in CHARACTER_HEADER_FIELDS.keys()]
