"""Top-Level Audit Class"""
import logging
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests
# We'll need this if we want to setup retries
# from requests.packages.urllib3.util.retry import Retry

from wowapi import WowApi

from .utility import Utility
from .models import Class, Faction, Race, Region, Realm, Character, Gem
from .blizzard import BLIZZARD_REGION, BLIZZARD_LOCALE
from .gem_enchant import gem_lookup
from .processing import process_blizzard, process_raiderio, serialize
from . import sections as Section

RAIDERIO_URL="https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={character_name}&fields=mythic_plus_scores_by_season:current,mythic_plus_highest_level_runs,mythic_plus_weekly_highest_level_runs"

def _character_as_dict(character):
    return {'character_name' : character.name,
            'realm' : character.realm_slug,
            'region' : character.region_name}

class Audit:
    """
    Top-Level class Responsible for managing the system.

    This class will hold all necessary data across multiple refreshes
    """

    def __init__(self, config, sql_echo=False):
        self.engine = create_engine(config['database'], echo=sql_echo)
        self.blizzard_api = WowApi(**config['api']['blizzard'],
                retry_conn_failures=True)
        self.request_session = requests.Session()
        self.config_characters = config['characters']

    def setup_database(self):
        # Tables should be created via alembic, not here, as that will prevent
        # database migrations from working
        # Run 'alembic upgrade head' from command-line to create tables

        session = sessionmaker(self.engine)()

        try:
            self._create_classes(session)
            self._create_races(session)
            self._create_gems(session)

            self._remove_old_characters(session)
            self._add_missing_characters(session)

            self._remove_empty_realms(session)
            self._remove_empty_regions(session)

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def _create_classes(self, session):
        session.query(Class).delete()
        classes = self.blizzard_api.get_playable_classes(BLIZZARD_REGION,
                'static-' + BLIZZARD_REGION, locale=BLIZZARD_LOCALE)['classes']
        session.add_all([Class(c['name'], id=c['id']) for c in classes])

    def _create_races(self, session):
        session.query(Race).delete()
        session.query(Faction).delete()
        races = self.blizzard_api.get_playable_race_index(BLIZZARD_REGION,
                'static-' + BLIZZARD_REGION, locale=BLIZZARD_LOCALE)['races']

        for r in races:
            details = self.blizzard_api.get_data_resource("{}&locale={}".format(r['key']['href'], BLIZZARD_LOCALE), BLIZZARD_REGION)

            race_faction = session.query(Faction).filter_by(name=details['faction']['name']).first()

            if not race_faction:
                race_faction = Faction(details['faction']['name'])

            session.add(
                    Race(details['name'], id=details['id'],faction=race_faction))

    def _create_gems(self, session):
        for id, details in gem_lookup.items():
            if session.query(Gem).filter_by(id=id).first() == None:
                g = Gem(id, **details)
                session.add(g)

    def _remove_old_characters(self, session):
        config_characters = [{'name' : character, 'realm' : realm, 'region' : region}
                for region,realms in self.config_characters.items()
                for realm,characters in realms.items()
                for character in characters]

        stored_characters = session.query(Character).all()

        for char in stored_characters:
            if not {'name' : char.name, 'realm' : char.realm_name, 'region' : char.region_name} in config_characters:
                session.delete(char)

    def _add_missing_characters(self, session):
        for region,realms in self.config_characters.items():
            region_model = session.query(Region).filter_by(name=region).first()
            if not region_model:
                region_model = Region(region)
                session.add(region_model)

            for realm,characters in realms.items():
                realm_model = session.query(Realm).filter_by(name=realm).join(Region).filter_by(name=region).first()
                if not realm_model:
                    realm_model = Realm(realm, region_model)
                    session.add(realm_model)

                for character in characters:
                    character_model = session.query(Character).\
                            filter_by(name=character).join(Realm).\
                            filter_by(name=realm).join(Region).\
                            filter_by(name=region).first()

                    if not character_model:
                        character_model = Character(character, realm=realm_model)
                        session.add(character_model)

    def _remove_empty_realms(self, session):
        empty = session.query(Realm).filter(~Realm.characters.any()).all()
        for r in empty:
            session.delete(r)

    def _remove_empty_regions(self, session):
        empty = session.query(Region).filter(~Region.realms.any()).all()
        for r in empty:
            session.delete(r)

    def refresh(self, dt, force_refresh=False):
        """
        Refresh each character

        @param dt The datetime.datetime module
        """
        Utility.set_refresh_timestamp(dt.utcnow())

        session = sessionmaker(self.engine)()

        logger = logging.getLogger('altaudit')

        try:
            characters = session.query(Character).all()

            output = [Section.metadata()]
            for character in characters:
                logger.debug("%s:%s:%s", character.region_name, character.realm_slug, character.name)
                try:
                    profile = { 'summary' : self.blizzard_api.get_character_profile_summary(**_character_as_dict(character),
                        namespace="profile-{}".format(character.region_name),
                        locale=BLIZZARD_LOCALE) }
                    rio_resp = self.request_session.get(RAIDERIO_URL.format(**_character_as_dict(character)))

                    process_blizzard(character, profile, session, self.blizzard_api, force_refresh)
                    process_raiderio(character, rio_resp)
                    session.commit()
                except:
                    logger.error("%s Failed", character.name)
                    logger.exception(traceback.format_exc())
                    session.rollback()
                finally:
                    output.append(serialize(character))

        except:
            logger.error('Critical failure in character processing')
            session.rollback()
            raise
        finally:
            session.close()

        return output
