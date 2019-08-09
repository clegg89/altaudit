"""Pull Reputation data from API"""

def reputations(character, response):
    # TODO move to constants with commnents on who each is
    reputations = {
                'alliance' : [2160, 2162, 2161, 2159, 2164, 2163, 2400, 2391],
                'hoard' : [2103, 2156, 2158, 2157, 2164, 2163, 2373, 2391]
            }
    reputation_response = response['reputation']
    faction = character.faction_name

    result = ''
    for rep in reputations[faction]:
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
