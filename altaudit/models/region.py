"""Region Model"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base, IdMixin
from .realm import Realm

class Region(IdMixin, Base):
    __tablename__ = 'regions'

    name = Column(String)

    realms = relationship('Realm', backref='region',
            cascade='all, delete, delete-orphan')

    def __init__(self, name):
        self.name = name
