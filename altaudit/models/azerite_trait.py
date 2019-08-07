"""Model representing Azerite Traits"""
from sqlalchemy import Column, Integer, String

from .base import Base

class AzeriteTrait(Base):
    __tablename__ = 'azerite_traits'

    spell_id = Column(Integer)
    name = Column(String)
    icon = Column(String)

    def __init__(self, id, spell_id, name, icon):
        self.id = id
        self.spell_id = spell_id
        self.name = name
        self.icon = icon
