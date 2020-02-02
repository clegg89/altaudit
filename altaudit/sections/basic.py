"""Pull Basic Character Data from API Response"""

from ..models import Class, Faction, Race

def basic(character, response, db_session):
    character.name_api = response['name']
    character.realm_name = response['realm']['name']
    character.lastmodified = response['last_login_timestamp']
    character.character_class = db_session.query(Class).filter_by(name=response['character_class']['name']).first()
    character.level = response['level']
    character.mainspec = response['active_spec']['name']
    character.faction = db_session.query(Faction).filter_by(name=response['faction']['name']).first()
    character.gender = response['gender']['name']
    character.race = db_session.query(Race).filter_by(name=response['race']['name']).first()
    # character.avatar = response['thumbnail']
    # character.bust = response['thumbnail'].replace('avatar', 'inset')
    # character.render = response['thumbnail'].replace('avatar', 'main')
