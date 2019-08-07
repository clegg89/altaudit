"""Model representing Characters"""
from sqlalchemy import Table, Column, UniqueConstraint, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from ..constants import CHARACTER_HEADER_FIELDS, AZERITE_ITEM_SLOTS, AZERITE_TIERS
from ..utility import Utility

from .base import Base
from .azerite_trait import AzeriteTrait
from .snapshot import Year, Snapshot

"""
Each Character has multiple AzeriteTraits available for each AZERITE_TIERS within each AZERITE_ITEM_SLOTS.

This leaves us with two options for our model:

    - Create a join table for each slot+tier combo. This will lead to a total of 15 tables. Each table
    can be referenced via a relationship attribute in Character
    - Create a single join table that joins a 'slot+tier' table. Character will then contain foreign keys
    for each slot+tier to the slot+tier table, and can use association_proxy to get to its various traits

I don't actually know enough about relational databases to know what the trade-offs are. You'd assume that
the former gives better runtime performance but who the hell knows. I'm going to opt for it because it
seems cleaner: There's not really a reason to avoid a lot of tables and it means I don't have to add even
more foreign keys to the Character Model.

As a side note: we could potentially have a join table for the other 'foreign key' attributes in Character.
This would mean removing said keys would mean dropping tables instead of removing fields from Character.
Probably not worth it since its a bit more verbose, but still worth noting.
"""
for slot in AZERITE_ITEM_SLOTS:
    for tier in range(AZERITE_TIERS):
        var = '{}_tier{}'.format(slot, tier)
        var_name = 'character_trait_{}_association'.format(var)
        table_name = 'characters_traits_{}'.format(var)
        exec("""{} = Table('{}', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('azerite_trait_id', Integer, ForeignKey('azerite_traits.id')))""".format(var_name, table_name))

class Character(Base):
    __tablename__ = 'characters'

    realm_id = Column(Integer, ForeignKey('realms.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    faction_id = Column(Integer, ForeignKey('factions.id'))
    race_id = Column(Integer, ForeignKey('races.id'))
    character_class = relationship('Class')
    faction = relationship('Faction')
    race = relationship('Race')

    for slot in AZERITE_ITEM_SLOTS:
        for tier in range(AZERITE_TIERS):
            slot_tier = '{}_tier{}'.format(slot, tier)
            selected = '{}_selected'.format(slot_tier)
            selected_fk = '{}_id'.format(selected)
            selected_rel = '_{}'.format(selected) # Precede with underscore to distinguish from Header
            available_sec = 'character_trait_{}_association'.format(slot_tier)
            available_rel = '_{}_available'.format(slot_tier) # Precede with underscore to distinguish from Header

            exec("{} = Column(Integer, ForeignKey('azerite_traits.id'))".format(selected_fk))
            exec("{} = relationship('AzeriteTrait', foreign_keys=[{}])".format(selected_rel, selected_fk))
            exec("{} = relationship('AzeriteTrait', secondary={})".format(available_rel, available_sec))

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
