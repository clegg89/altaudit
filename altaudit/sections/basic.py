"""Pull Basic Character Data from API Response"""

from ..models import Class, Faction, Race

def basic(character, response, db_session):
    character.name_api = response['name']
    character.realm_name = response['realm']
    character.lastmodified = response['lastModified']
    character.character_class = db_session.query(Class).filter_by(id=response['class']).first()
    character.level = response['level']
    character.mainspec = _find_mainspec(response)
    character.faction = db_session.query(Faction).filter_by(id=response['faction']+1).first()
    character.gender = 'Male' if response['gender'] == 0 else 'Female' if response['gender'] == 1 else None
    character.race = db_session.query(Race).filter_by(id=response['race']).first()
    character.avatar = response['thumbnail']
    character.bust = response['thumbnail'].replace('avatar', 'inset')
    character.render = response['thumbnail'].replace('avatar', 'main')
    # db_session.flush()

def _find_mainspec(response):
    mainspec = None
    for spec in response['talents']:
        if 'selected' in spec and spec['selected']:
            mainspec = spec['spec']['name']

    return mainspec
