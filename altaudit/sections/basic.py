"""Pull Basic Character Data from API Response"""

from ..blizzard import BLIZZARD_LOCALE
from ..models import Class, Faction, Race

def basic(character, profile, db_session, api):
    """
    Basic character information. If some of these fields are not
    present, we will just fail, as we don't want to update the character
    if they are missing
    """
    character.name_api = profile['summary']['name']
    character.realm_name = profile['summary']['realm']['name']
    character.lastmodified = profile['summary']['last_login_timestamp']
    character.character_class = db_session.query(Class).filter_by(name=profile['summary']['character_class']['name']).first()
    character.level = profile['summary']['level']
    character.mainspec = profile['summary']['active_spec']['name'] if 'active_spec' in profile['summary'] else None
    character.faction = db_session.query(Faction).filter_by(name=profile['summary']['faction']['name']).first()
    character.gender = profile['summary']['gender']['name']
    character.race = db_session.query(Race).filter_by(name=profile['summary']['race']['name']).first()

    assets = profile['media']['assets']
    character.avatar = next((asset['value'] for asset in assets if asset['key'] == 'avatar'), None)
    character.bust = next((asset['value'] for asset in assets if asset['key'] == 'inset'), None)
    character.render = next((asset['value'] for asset in assets if asset['key'] == 'main'), None)
