"""Realm Model"""
from sqlalchemy import Column, UniqueConstraint, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base, IdMixin
from .character import Character

class Realm(IdMixin, Base):
    __tablename__ = 'realms'

    region_id = Column(Integer, ForeignKey('regions.id'))
    name = Column(String)

    __table_args__ = (UniqueConstraint('region_id', 'name'),)

    region_name = association_proxy('region', 'name')
    characters = relationship('Character', backref='realm',
            cascade='all, delete, delete-orphan')

    def __init__(self, name, region=None):
        self.name = name
        if region:
            self.region = region
