"""Pull Reputation data from API"""

from ..constants import REPUTATION_FACTION_ID

def reputations(character, response):
    reputation_response = response['reputation']
    faction = character.faction_name

    result = ''
    for rep in REPUTATION_FACTION_ID[faction]:
        # Find the reputation dictionary where 'id' is our rep
        rep_data = next((d for d in reputation_response if d['id'] == rep), None)
        if rep_data:
            result += '{}+{}+{}+{}+{}|'.format(rep_data['id'],
                    rep_data['name'],
                    rep_data['standing'],
                    rep_data['value'],
                    rep_data['max'])
        else:
            result += '++++|'

    character.reputations = result[:-1]
