"""Top-Level Audit Class"""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests
# We'll need this if we want to setup retries
# from requests.packages.urllib3.util.retry import Retry

from wowapi import WowApi

from .utility import Utility
from .models import Class, Faction, Race, Region, Realm, Character, Gem
from .constants import BLIZZARD_REGION, BLIZZARD_LOCALE, BLIZZARD_CHARACTER_FIELDS, RAIDERIO_URL
from .gem_enchant import gem_lookup
from . import sections as Section

def _character_as_dict(character):
    return {'character_name' : character.name,
            'realm' : character.realm_slug,
            'region' : character.region_name}

class Audit:
    """
    Top-Level class Responsible for managing the system.

    This class will hold all necessary data across multiple refreshes
    """

    def __init__(self, config, retry_conn_failures=False, sql_echo=False):
        self.engine = create_engine(config['database'], echo=sql_echo)
        self.blizzard_api = WowApi(**config['api']['blizzard'],
                retry_conn_failures=retry_conn_failures)
        self.request_session = requests.Session()
        self.config_characters = config['characters']

    def setup_database(self):
        # Tables should be created via alembic, not here, as that will prevent
        # database migrations from working
        # Run 'alembic upgrade head' from command-line to create tables

        session = sessionmaker(self.engine)()

        try:
            self._create_factions(session)
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

    def _create_factions(self, session):
        session.query(Faction).delete()
        for i,v in enumerate(['Alliance', 'Horde', 'Neutral']):
            f = Faction(v, id=i+1)
            session.add(f)

    def _create_classes(self, session):
        session.query(Class).delete()
        classes = self.blizzard_api.get_character_classes(BLIZZARD_REGION, locale=BLIZZARD_LOCALE)['classes']
        session.add_all([Class(c['name'], id=c['id']) for c in classes])

    def _create_races(self, session):
        session.query(Race).delete()
        races = self.blizzard_api.get_character_races(BLIZZARD_REGION, locale=BLIZZARD_LOCALE)['races']

        fquery = session.query(Faction)
        session.add_all([
            Race(r['name'], id=r['id'],
                faction=fquery.filter_by(name=r['side'].capitalize()).first())
            for r in races])

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
                logger.info("%s:%s:%s", character.region_name, character.realm_slug, character.name)
                blizz_resp = self.blizzard_api.get_character_profile(**_character_as_dict(character),
                    locale=BLIZZARD_LOCALE,
                    fields=','.join(BLIZZARD_CHARACTER_FIELDS))
                rio_resp = self.request_session.get(RAIDERIO_URL.format(**_character_as_dict(character)))

                character.process_blizzard(blizz_resp, session, self.blizzard_api, force_refresh)
                character.process_raiderio(rio_resp)
                output.append(character.serialize())

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return output
