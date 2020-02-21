"""Model representing Characters"""
from sqlalchemy import Table, Column, UniqueConstraint, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from wowapi import WowApiException

from .base import Base
from .azerite_trait import AzeriteTrait
from .gem import Gem
from .gem_slot_association import GemSlotAssociation
from .snapshot import Year, Snapshot

"Item slots tracked"
ITEM_SLOTS = [
    'head', 'neck', 'shoulder', 'back',
    'chest', 'wrist', 'hands', 'waist',
    'legs', 'feet', 'finger_1', 'finger_2',
    'trinket_1', 'trinket_2', 'main_hand', 'off_hand'
]

"Item Fields to use in Character Model"
ITEM_FIELD_COLUMNS = [
    ('itemLevel','Column(Integer)'),
    ('id', 'Column(Integer)'),
    ('name', 'Column(String)'),
    ('quality', 'Column(String)')]

"Item Fields"
ITEM_FIELDS = [field[0] for field in ITEM_FIELD_COLUMNS]

"Azerite piece item slots"
AZERITE_ITEM_SLOTS = [ 'head', 'shoulder', 'chest' ]

"Number of Azerite Tiers"
AZERITE_TIERS = 5

"Item slots that can be enchanted (for BfA)"
ENCHANTED_ITEM_SLOTS = [ 'main_hand', 'off_hand', 'finger_1', 'finger_2', 'hands', 'wrist' ]

"Item Enchant filds for use in Character Model"
ENCHANT_ITEM_FIELD_COLUMNS = [
        ('id', 'Column(Integer)'),
        ('quality', 'Column(Integer)'),
        ('name', 'Column(String)'),
        ('description', 'Column(String)')]

"Professions, excluding Archaeology"
PROFESSIONS = ['primary1', 'primary2', 'cooking', 'fishing']

"List of all expacs and their profession prefix"
PROFESSION_EXPACS = {
    '' : 'classic',
    'Outland' : 'burning_crusade',
    'Northrend' : 'wrath_of_the_lich_king',
    'Cataclysm' : 'cataclysm',
    'Pandaria' : 'mists_of_pandaria',
    'Draenor' : 'warlords_of_draenor',
    'Legion' : 'legion',
    'Kul Tiran' : 'battle_for_azeroth'}

"WoW expansions"
EXPACS = [v for v in PROFESSION_EXPACS.values()]

"Profession Field Columns excluding Archaeology"
PROFESSION_FIELD_COLUMNS = [
    ('name', 'Column(String)'),
    ('icon', 'Column(String)'),
    *[('{}_{}'.format(expac, f), 'Column(Integer)')
        for expac in EXPACS for f in ['level', 'max']]]

"Archaeology Field Columns"
ARCHAEOLOGY_FIELD_COLUMNS = [
    ('name', 'Column(String)'),
    ('icon', 'Column(String)'),
    ('level', 'Column(Integer)'),
    ('max', 'Column(Integer)')]

"Raid Difficulties"
RAID_DIFFICULTIES = [
    'raid_finder', 'normal', 'heroic', 'mythic'
]

"Column Headers and their database types"
CHARACTER_HEADER_FIELDS = {
    # Basic Info
    'name_api' : 'Column(String)',
    'realm_name' : "Column(Integer)",
    'realm_slug' : "association_proxy('realm', 'name')",
    'region_name' : "association_proxy('realm', 'region_name')",
    'lastmodified' : 'Column(Integer)',
    'class_name' : "association_proxy('character_class', 'name')",
    'level' : 'Column(Integer)',
    'mainspec' : 'Column(String)',
    'faction_name' : "association_proxy('faction', 'name')",
    'gender' : 'Column(String)',
    'race_name' : "association_proxy('race', 'name')",
    'avatar' : 'Column(String)',
    'bust' : 'Column(String)',
    'render' : 'Column(String)',

    # Item Info
    'estimated_ilvl' : 'Column(Float)',

    **{'{}_{}'.format(slot, item[0]) : item[1]
        for slot in ITEM_SLOTS
        for item in ITEM_FIELD_COLUMNS},

    # Azerite Info
    'hoa_level' : 'Column(Integer)',
    'azerite_percentage' : 'Column(Float)',

    **{'{}_tier{}_{}'.format(piece, tier, field) : "''" # Composite from azerite_traits table
        for piece in AZERITE_ITEM_SLOTS
        for tier in range(AZERITE_TIERS)
        for field in ['available', 'selected']},

    # Gear Audit
    **{'{}_enchant_{}'.format(slot, field[0]) : field[1]
        for slot in ENCHANTED_ITEM_SLOTS
        for field in ENCHANT_ITEM_FIELD_COLUMNS},

    'empty_sockets' : 'Column(Integer)',

    **{'gem_{}'.format(field) : "''" # Composite from gems table
        for field in ['ids', 'qualities', 'names', 'icons', 'stats', 'slots']},

    # Profession Info
    **{'{}_{}'.format(prof, field[0]) : field[1]
        for prof in PROFESSIONS
        for field in PROFESSION_FIELD_COLUMNS},

    **{'archaeology_{}'.format(field[0]) : field[1] for field in
        ARCHAEOLOGY_FIELD_COLUMNS},

    # Reputations
    'reputations' : 'Column(String)',

    # PvE and RaiderIO
    'island_weekly_done' : 'Column(String)',
    'islands_total' : 'Column(Integer)',
    'world_quests_total' : 'Column(Integer)',
    'world_quests_weekly' : "None", # Obtained from snapshots
    'weekly_event_done' : 'Column(String)',
    'dungeons_total' : 'Column(Integer)',
    'dungeons_each_total' : 'Column(String)',
    'dungeons_weekly' : "None", # Obtained from snapshots
    'raiderio_score' : 'Column(Float)',
    'mplus_weekly_highest' : 'Column(Integer)',
    'mplus_season_highest' : 'Column(Integer)',

    **{'raids_{}{}'.format(difficulty,postfix) : 'Column(String)'
            for difficulty in RAID_DIFFICULTIES
            for postfix in ('','_weekly')}
}

HEADERS = [k for k in CHARACTER_HEADER_FIELDS.keys()]

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

    name = Column(String)
    realm_id = Column(Integer, ForeignKey('realms.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))
    faction_id = Column(Integer, ForeignKey('factions.id'))
    race_id = Column(Integer, ForeignKey('races.id'))
    character_class = relationship('Class')
    faction = relationship('Faction')
    race = relationship('Race')

    for slot in AZERITE_ITEM_SLOTS:
        for tier in range(AZERITE_TIERS):
            # Relationships are _SLOT_tierNUMBER_selected and _SLOT_tierNUMBER_available
            slot_tier = '{}_tier{}'.format(slot, tier)
            selected = '{}_selected'.format(slot_tier)
            selected_fk = '{}_id'.format(selected)
            selected_rel = '_{}'.format(selected) # Precede with underscore to distinguish from Header
            available_sec = 'character_trait_{}_association'.format(slot_tier)
            available_rel = '_{}_available'.format(slot_tier) # Precede with underscore to distinguish from Header

            exec("{} = Column(Integer, ForeignKey('azerite_traits.id'))".format(selected_fk))
            exec("{} = relationship('AzeriteTrait', foreign_keys=[{}])".format(selected_rel, selected_fk))
            exec("{} = relationship('AzeriteTrait', secondary={})".format(available_rel, available_sec))

    gems = relationship('GemSlotAssociation', cascade='all, delete, delete-orphan')

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
