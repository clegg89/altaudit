"""Unit Tests for the Region Model"""
import pytest

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from charfetch.models.region import Region

def test_create_region_table():
    path = os.path.dirname(os.path.realpath(__file__))
    engine = create_engine("sqlite:///{}/test.db".format(path))
    Session = sessionmaker(engine)
    session = Session()
    Region.__table__.create(engine)
    assert engine.has_table('regions')
    Region.__table__.drop(engine)
