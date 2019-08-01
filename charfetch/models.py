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

class Region(Base):
    __tablename__ = 'regions'

    name = Column(String)

    realms = relationship('Realm', backref='region')


class Realm(Base):
    __tablename__ = 'realms'

    region_id = Column(Integer, ForeignKey('regions.id'))
    name = Column(String)
    slug = Column(String)

    characters = relationship('Character', backref='realm')

class Character(Base):
    __tablename__ = 'characters'

    realm_id = Column(Integer, ForeignKey('realms.id'))
    name = Column(String)

    for k,v in CHARACTER_HEADER_FIELDS.items():
        exec('{} = Column({})'.format(k,v))

    years = relationship("Year", backref='character',
            collection_class=attribute_mapped_collection('year'))

    def _creator(k, v):
        y = Year(k)
        y.snapshots = v
        return y

    snapshots = association_proxy('years', 'snapshots',
            creator=_creator)

class Year(Base):
    __tablename__ = 'years'

    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    year = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('character_id', 'year'),)

    weeks = relationship('Week', backref='year',
            collection_class=attribute_mapped_collection('week'))

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

    snapshot = relationship("Snapshot", uselist=False, backref='week')

    def __init__(self, week):
        self.week = week

class Snapshot(Base):
    __tablename__ = 'snapshots'

    week_id = Column(Integer, ForeignKey('weeks.id'), nullable=False)
