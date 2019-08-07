"""Model representing Characters"""
from sqlalchemy import Column, UniqueConstraint, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from ..constants import CHARACTER_HEADER_FIELDS
from ..utility import Utility

from .base import Base
from .snapshot import Year, Snapshot

class Character(Base):
    __tablename__ = 'characters'

    realm_id = Column(Integer, ForeignKey('realms.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    faction_id = Column(Integer, ForeignKey('factions.id'))
    race_id = Column(Integer, ForeignKey('races.id'))
    character_class = relationship('Class')
    faction = relationship('Faction')
    race = relationship('Race')

    for k,v in CHARACTER_HEADER_FIELDS.items():
        exec('{} = {}'.format(k,v))

    __table_args__ = (UniqueConstraint('realm_id', 'name'),)

    years = relationship("Year", backref='character',
            collection_class=attribute_mapped_collection('year'),
            cascade='all, delete, delete-orphan')

    def _creator(k, v):
        y = Year(k)
        y.snapshots = v
        return y

    snapshots = association_proxy('years', 'snapshots',
            creator=_creator)

    def __init__(self, name, **kwargs):
        self.name = name

        for k,v in kwargs.items():
            if k in CHARACTER_HEADER_FIELDS or \
            hasattr(self, k):
                self.__setattr__(k, v)

    def update_snapshot(self):
        year = Utility.year[self.region_name]
        week = Utility.week[self.region_name]
        if year not in self.snapshots:
            self.snapshots[year] = {}

        if week not in self.snapshots[year]:
            self.snapshots[year][week] = Snapshot()

    def process_blizzard(self, response, api):
        """
        Processes the response from blizzard's API for this character

        @param response The response from blizzard's api

        @param api The api object used to make the request

        @returns True if the character needs to be updated, False otherwise
        """
        if response['lastModified'] == self.lastmodified:
            # Already up-to-date
            return False

    def process_raiderio(self, response):
        """
        Processes the response from raider.io API for this character

        @param response The response from raider.io's API

        """
        pass
