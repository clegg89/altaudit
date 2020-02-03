"""Pull Basic Character Data from API Response"""

from ..constants import BLIZZARD_LOCALE
from ..models import Class, Faction, Race

def basic(character, profile, db_session, api):
    character.name_api = profile['summary']['name']
    character.realm_name = profile['summary']['realm']['name']
    character.lastmodified = profile['summary']['last_login_timestamp']
    character.character_class = db_session.query(Class).filter_by(name=profile['summary']['character_class']['name']).first()
    character.level = profile['summary']['level']
    character.mainspec = profile['summary']['active_spec']['name']
    character.faction = db_session.query(Faction).filter_by(name=profile['summary']['faction']['name']).first()
    character.gender = profile['summary']['gender']['name']
    character.race = db_session.query(Race).filter_by(name=profile['summary']['race']['name']).first()

    if api:
        profile['media'] = api.get_data_resource(
                '{}&locale={}'.format(profile['summary']['media'], BLIZZARD_LOCALE),
                character.region_name)

        character.avatar = profile['media']['avatar_url']
        character.bust = profile['media']['bust_url']
        character.render = profile['media']['render_url']
