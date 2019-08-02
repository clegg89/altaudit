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

        session.query(Class).delete()
        session.query(Race).delete()

        classes = self.api.get_character_classes('us', locale='en_US')['classes']
        races = self.api.get_character_races('us', locale='en_US')['races']

        session.add_all([Class(c['name'], id=c['id']) for c in classes])
        session.add_all([Race(r['name'], id=r['id']) for r in races])

    def refresh(self):
        "Refresh each character and write the result to the server"
        pass
