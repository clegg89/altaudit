"""Models for database"""
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from charfetch.constants import CHARACTER_HEADER_FIELDS

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    realms = relationship('Realm', backref='region')


class Realm(Base):
    __tablename__ = 'realms'

    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    name = Column(String)
    slug = Column(String)

    characters = relationship('Character', backref='realm')

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    realm_id = Column(Integer, ForeignKey('realms.id'))
    name = Column(String)

    for k,v in CHARACTER_HEADER_FIELDS.items():
        exec('{} = Column({})'.format(k,v))
