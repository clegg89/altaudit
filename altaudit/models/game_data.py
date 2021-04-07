"""Models representing game data"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base

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

