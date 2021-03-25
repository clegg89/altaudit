""" Pull Covenant Information from the API and fill in character model """

def covenant(character, profile, db_session):
    character.covenant = profile['summary']['covenant_progress']['chosen_covenant']['name']
