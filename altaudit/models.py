"""Models for database"""
from sqlalchemy import Column, UniqueConstraint, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

from charfetch.constants import CHARACTER_HEADER_FIELDS

class Base(object):
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

class Class(Base):
    __tablename__ = 'classes'

    name = Column(String)

    def __init__(self, name, id=None):
        self.name = name
        if id:
            self.id = id

class Faction(Base):
    __tablename__ = 'factions'

    name = Column(String)

    def __init__(self, name, id=None):
        self.name = name
        if id:
            self.id = id

class Race(Base):
    __tablename__ = 'races'

    faction_id = Column(Integer, ForeignKey('factions.id'))
    name = Column(String)

    faction = relationship('Faction')
    faction_name = association_proxy('faction', 'name')

    def __init__(self, name, **kwargs):
        self.name = name

        for k,v in kwargs.items():
            if hasattr(self, k):
                self.__setattr__(k, v)

class Region(Base):
    __tablename__ = 'regions'

    name = Column(String)

    realms = relationship('Realm', backref='region',
            cascade='all, delete, delete-orphan')

    def __init__(self, name):
        self.name = name

class Realm(Base):
    __tablename__ = 'realms'

    region_id = Column(Integer, ForeignKey('regions.id'))
    name = Column(String)

    region_name = association_proxy('region', 'name')
    characters = relationship('Character', backref='realm',
            cascade='all, delete, delete-orphan')

    def __init__(self, name, region=None):
        self.name = name
        if region:
            self.region = region

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

class Year(Base):
    __tablename__ = 'years'

    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    year = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('character_id', 'year'),)

    weeks = relationship('Week', backref='year',
            collection_class=attribute_mapped_collection('week'),
            cascade='all, delete, delete-orphan')

    def _creator(k, v):
        w = Week(k)
        w.snapshot = v
        return w

    snapshots = association_proxy('weeks', 'snapshot',
            creator=_creator)

    def __init__(self, year):
        self.year = year

class Week(Base):
    __tablename__ = 'weeks'

    year_id = Column(Integer, ForeignKey('years.id'), nullable=False)
    week = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('year_id', 'week'),)

    snapshot = relationship("Snapshot", uselist=False, backref='week',
            cascade='all, delete, delete-orphan')

    def __init__(self, week):
        self.week = week

class Snapshot(Base):
    __tablename__ = 'snapshots'

    week_id = Column(Integer, ForeignKey('weeks.id'), nullable=False)
    world_quests = Column(Integer)
    dungeons = Column(Integer)
    azerite_power = Column(Integer)
