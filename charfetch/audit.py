"""Top-Level Audit Class"""
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wowapi import WowApi

from .models import Base, Class, Races

class Audit:
    """
    Top-Level class Responsible for managing the system.

    This class will hold all necessary data across multiple refreshes
    """

    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        self.engine = create_engine(config['database'])
        self.blizzard_api = WowApi(**config['api']['blizzard'])

        self.server = config['server']

        Base.metadata.create_all(self.engine)

        session = sessionmaker(self.engine)()

        if session.query(Faction).count() != 3:
            session.query(Faction).delete()
            for i,v in ['alliance', 'horde', 'neutral']:
                f = Faction(v, id=i)
                session.add(f)

        session.query(Class).delete()
        session.query(Race).delete()

        classes = self.api.get_character_classes('us', locale='en_US')['classes']
        races = self.api.get_character_races('us', locale='en_US')['races']

        session.add_all([Class(c['name'], id=c['id']) for c in classes])
        session.add_all([Race(r['name'], id=r['id']) for r in races])

        config_characters = [{'name' : character, 'realm' : realm, 'region' : region}
                for region,realms in config['characters'].items()
                for realm,characters in realm.items()
                for character in characters]

        stored_characters = session.query(Character).all()

        for char in stored_characters:
            if not {'name' : char.name, 'realm' : char.realm_name, 'region' : char.region_name} in config_characters:
                session.delete(char)

        for region,realms in data.items():
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
                            filter_by(name=character).\
                            join(Realm).filtery_by(name=realm).\
                            join(Region).filter_by(name=region).first()

                    if not character_model:
                        character_model = Character(character, realm=realm, region=region)
                        session.add(character_model)

        session.commit()
        session.close()

    def refresh(self):
        "Refresh each character and write the result to the server"
        pass
