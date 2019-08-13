"""Region Model"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base

class Region(Base):
    __tablename__ = 'regions'

    name = Column(String)

    realms = relationship('Realm', backref='region',
            cascade='all, delete, delete-orphan')

    def __init__(self, name):
        self.name = name
