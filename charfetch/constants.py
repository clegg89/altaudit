"""Charfetch Program Constants"""

"Item slots tracked"
ITEM_SLOTS = [
    'head', 'neck', 'shoulder', 'back',
    'chest', 'wrist', 'hands', 'waist',
    'legs', 'feet', 'finger1', 'finger2',
    'trinket1', 'trinket2', 'mainHand', 'offHand'
]

"WoW expansions"
EXPACS = [
    'classic', 'burning_crusade', 'wrath_of_the_lich_king',
    'cataclysm', 'mists_of_pandaria', 'warlords_of_draenor',
    'legion', 'battle_for_azeroth'
]

"Column Headers and their database types"
CHARACTER_HEADER_FIELDS = {
    'lastmodified' : 'Integer',
    'klass' : 'String',
    'level' : 'Integer',
    'mainspec' : 'String',
    'faction' : 'String',
    'gender' : 'String',
    'race' : 'String',
    'avatar' : 'String',
    'bust' : 'String',
    'render' : 'String',
    'estimated_ilvl' : 'Numeric',

    **{'{}_{}'.format(slot, item[0]) : item[1]
        for slot in ITEM_SLOTS
        for item in [
            ('ilvl','Integer'),
            ('id', 'Integer'),
            ('name', 'String'),
            ('icon', 'String'),
            ('quality', 'Integer')]},

    'hoa_level' : 'Integer',
    'azerite_experience' : 'Integer',
    'azerite_experience_remaining' : 'Integer',
    'azerite_this_week' : 'Integer',

    **{'{}_tier{}_{}'.format(piece, tier, field) : 'String'
        for piece in ['head', 'shoulder', 'chest']
        for tier in range(5)
        for field in ['available', 'selected']},

    **{'{}_enchant_{}'.format(slot, field[0]) : field[1]
        for slot in ['mainHand', 'offHand', 'finger1', 'finger2', 'hand', 'wrist']
        for field in [('id', 'Integer'), ('quality', 'Integer'), ('name', 'String'), ('description', 'String')]},

    'empty_sockets' : 'Integer',

    **{'gem_{}'.format(field) : 'String'
        for field in ['ids', 'qualities', 'names', 'icons', 'stats', 'slots']},

    **{'{}_{}'.format(prof, field[0]) : field[1]
        for prof in ['primary1', 'primary2', 'cooking', 'fishing']
        for field in [('name', 'String'), ('icon', 'String'),
            *[('{}_{}'.format(expac, f), 'Integer')
                for expac in EXPACS for f in ['level', 'max']]]},

    **{'archaeology_{}'.format(field[0]) : field[1] for field in
        [('name', 'String'), ('icon', 'String'), ('level', 'Integer'), ('max', 'Integer')]},

    'reputations' : 'String',
    'island_weekly_done' : 'String',
    'islands_total' : 'Integer',
    'world_quests_total' : 'Integer',
    'world_quests_weekly' : 'Integer',
    'weekly_event_done' : 'String',
    'dungeons_total' : 'Integer',
    'dungeons_each_total' : 'String',
    'dungeons_weekly' : 'Integer',
    'raiderio_score' : 'Numeric',
    'mplus_weekly_highest' : 'Integer',
    'mplus_season_highest' : 'Integer',

    **{'raids_{}'.format(difficulty) : 'String'
        for difficulty in ['lfr', 'nromal', 'heroic', 'mythic']}
}

HEADERS = [k for k in CHARACTER_HEADER_FIELDS.keys()]
