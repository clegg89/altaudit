"""Model for gem to character association table"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, IdMixin

class GemSlotAssociation(Base):
    "AssocaitionObject pattern used to store the slot of the gem"
    __tablename__ = 'characters_gems'
    character_id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    gem_id = Column(Integer, ForeignKey('gems.id'), primary_key=True)
    slot = Column(String)

    gem = relationship('Gem')

    def __init__(self, slot, gem=None):
        self.slot=slot
        if gem:
            self.gem = gem
