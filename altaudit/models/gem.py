"""Model for gems"""
from sqlalchemy import Column, Integer, String

from .base import Base, IdMixin

class Gem(IdMixin, Base):
    __tablename__ = 'gems'

    quality = Column(Integer)
    name = Column(String)
    icon = Column(String)
    stat = Column(String)

    def __init__(self, id, quality, name, icon, stat):
        self.id = id
        self.quality = quality
        self.name = name
        self.icon = icon
        self.stat = stat
