"""Base model used by other model classes"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IdMixin:
    id = Column(Integer, primary_key=True)
