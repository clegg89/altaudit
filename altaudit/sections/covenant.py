""" Pull Covenant Information from the API and fill in character model """

"""
Convert Conduit Rank to Item Level values
"""
CONDUIT_RANK_TO_ILVL = {
        1  : 145,
        2  : 158,
        3  : 171,
        4  : 184,
        5  : 200,
        6  : 213,
        7  : 226,
        8  : 239,
        9  : 252,
        10 : 265,
        11 : 278,
        12 : 291,
        13 : 304,
        14 : 317,
        15 : 330
}

def covenant(character, profile, db_session):
    try:
        character.covenant = profile['summary']['covenant_progress']['chosen_covenant']['name']
    except KeyError:
        character.covenant = None

    try:
        character.renown = profile['summary']['covenant_progress']['renown_level']
    except KeyError:
        character.renown = None

    try:
        soulbind = next((soulbind
            for soulbind in profile['soulbinds']['soulbinds']
            if 'is_active' in soulbind and soulbind['is_active']), None)

        if soulbind:
            character.current_soulbind = soulbind['soulbind']['name']

            conduits_found = 0

            for trait in soulbind['traits']:
                if 'conduit_socket' not in trait:
                    continue

                socket = trait['conduit_socket']['socket']

                conduits_found += 1

                setattr(character, 'conduit_{}_name'.format(conduits_found), socket['conduit']['name'])
                setattr(character, 'conduit_{}_id'.format(conduits_found), socket['conduit']['id'])
                setattr(character, 'conduit_{}_ilvl'.format(conduits_found), CONDUIT_RANK_TO_ILVL[socket['rank']])

    except KeyError:
        character.current_soulbind = None
