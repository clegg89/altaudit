"""Region Model"""
from sqlalchemy import Column, Integer, String

from charfetch.models import Base

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
