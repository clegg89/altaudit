"""Pull Reputation data from API"""

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

# TODO Possible to get paragon now if we want
def reputations(character, profile, db_session, api):
    """
    Get reputation data relevant to current expac.
    Don't fail in here
    """
    reputations = profile['reputations']['reputations']
    faction = character.faction_name.lower()

    result = ''
    for rep in REPUTATION_FACTION_ID[faction]:
        rep_data = next((d for d in reputations if d['faction']['id'] == rep), None)
        if rep_data:
            result += '{}+{}+{}+{}+{}|'.format(rep_data['faction']['id'],
                    rep_data['faction']['name'],
                    rep_data['standing']['name'],
                    rep_data['standing']['value'],
                    rep_data['standing']['max'])
        else:
            result += '++++|'

    character.reputations = result[:-1]
