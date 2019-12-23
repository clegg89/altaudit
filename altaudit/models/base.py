"""Base model used by other model classes"""
from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(naming_convention={
    "ix" : "ix_%(column_0_label)s",
    "uq" : "uq_%(table_name)s_%(column_0_N_name)s",
    "ck" : "ck_%(table_name)s_%(constraint_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk" : "pk_%(table_name)s"
})

class Base:
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base, metadata=meta)
