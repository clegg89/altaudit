"""Models representing snapshot information"""
from sqlalchemy import Column, UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base

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
