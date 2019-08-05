"""Top-Level Audit Class"""
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wowapi import WowApi

from .models import Base, Class, Faction, Race, Region, Realm, Character

# class AuditCharacter(Character):
#     "Extends the Character class to add in methods to process API responses"
#     def process_blizzard(self, response, api):
#         """
#         Processes the response from blizzard's API for this character

#         @param response The response from blizzard's api

#         @param api The api object used to make the request
#         """

class Audit:
    """
    Top-Level class Responsible for managing the system.

    This class will hold all necessary data across multiple refreshes
    """

    def __init__(self, config):
        self.engine = create_engine(config['database'])
        self.blizzard_api = WowApi(**config['api']['blizzard'])

        self.server = config['server']

        Base.metadata.create_all(self.engine)

        session = sessionmaker(self.engine)()

        self._create_factions(session)
        self._create_classes(session)
        self._create_races(session)

        self._remove_old_characters(session, config['characters'])
        self._add_missing_characters(session, config['characters'])

        self._remove_empty_realms(session)
        self._remove_empty_regions(session)

        session.commit()
        session.close()

    def _create_factions(self, session):
        session.query(Faction).delete()
        for i,v in enumerate(['Alliance', 'Horde', 'Neutral']):
            f = Faction(v, id=i+1)
            session.add(f)

    def _create_classes(self, session):
        session.query(Class).delete()
        classes = self.blizzard_api.get_character_classes('us', locale='en_US')['classes']
        session.add_all([Class(c['name'], id=c['id']) for c in classes])

    def _create_races(self, session):
        session.query(Race).delete()
        races = self.blizzard_api.get_character_races('us', locale='en_US')['races']

        fquery = session.query(Faction)
        session.add_all([
            Race(r['name'], id=r['id'],
                faction=fquery.filter_by(name=r['side'].capitalize()).first())
            for r in races])

    def _remove_old_characters(self, session, config):
        config_characters = [{'name' : character, 'realm' : realm, 'region' : region}
                for region,realms in config.items()
                for realm,characters in realms.items()
                for character in characters]

        stored_characters = session.query(Character).all()

        for char in stored_characters:
            if not {'name' : char.name, 'realm' : char.realm_name, 'region' : char.region_name} in config_characters:
                session.delete(char)

    def _add_missing_characters(self, session, config):
        for region,realms in config.items():
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
                        character_model = Character(character, realm=realm_model, region=region_model)
                        session.add(character_model)

    def _remove_empty_realms(self, session):
        empty = session.query(Realm).filter(~Realm.characters.any()).all()
        for r in empty:
            session.delete(r)

    def _remove_empty_regions(self, session):
        empty = session.query(Region).filter(~Region.realms.any()).all()
        for r in empty:
            session.delete(r)

    def refresh(self):
        # "Refresh each character"
        # session = sessionmaker(self.engine)()
        # characters = session.query(AuditCharacter).all()
        # for character in characters:
        #     response = self.blizzard_api.get_character_profile(character.region_name,
        #             character.realm_name, character.name, locale='en_US',
        #             fields='statistics,talents,reputation,items,achievements,audit,professions,quests')
        #     character.process_blizzard(response)
            # Do the same for rio and wcl
