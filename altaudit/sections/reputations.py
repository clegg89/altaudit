"""Pull Reputation data from API"""
import logging

"""
Faction IDs for Reputations

To find these, go to Character Reputations page and find
relevant expac reputations.
"""
REPUTATION_FACTION_ID = {
    'alliance' : [
        2407, # The Ascended (Bastion)
        2410, # The Undying Army (Maldraxxus)
        2413, # Court of Harvesters (Revendreth)
        2432, # Venari (Maw)
        2439, # The Avowed (Revendreth 2)
        2465, # The Wild Hunt (Ardenweald)
    ],
    'horde' : [
        2407, # The Ascended (Bastion)
        2410, # The Undying Army (Maldraxxus)
        2413, # Court of Harvesters (Revendreth)
        2432, # Venari (Maw)
        2439, # The Avowed (Revendreth 2)
        2465, # The Wild Hunt (Ardenweald)
    ]
}

# TODO Possible to get paragon now if we want
def reputations(character, profile, db_session, api):
    """
    Get reputation data relevant to current expac.
    Don't fail in here
    """
    try:
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

    except (TypeError, KeyError):
        logger = logging.getLogger('altaudit')
        logger.exception("Error in Reputation for {}".format(character.name))
