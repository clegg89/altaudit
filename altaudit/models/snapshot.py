"""Models representing snapshot information"""
from sqlalchemy import Column, UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base, IdMixin

class Year(IdMixin, Base):
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

    def __init__(self, year, character=None):
        self.year = year
        if character:
            self.character = character

class Week(IdMixin, Base):
    __tablename__ = 'weeks'

    year_id = Column(Integer, ForeignKey('years.id'), nullable=False)
    week = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('year_id', 'week'),)

    snapshot = relationship("Snapshot", uselist=False, backref='week',
            cascade='all, delete, delete-orphan')

    def __init__(self, week, year=None):
        self.week = week
        if year:
            self.year = year

class Snapshot(IdMixin, Base):
    __tablename__ = 'snapshots'

    # This data is a 'snapshot' of what these values were when the week began
    # They are not an indication of how many have been done this week, but
    # rather how many were done when this week started. We can then subtract
    # the total from this number
    week_id = Column(Integer, ForeignKey('weeks.id'), nullable=False, unique=True)
    world_quests = Column(Integer, default=0)
    dungeons = Column(Integer, default=0)
