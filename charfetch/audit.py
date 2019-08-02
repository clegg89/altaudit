"""Top-Level Audit Class"""
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Audit:
    """
    Top-Level class Responsible for managing the system.

    This class will hold all necessary data across multiple refreshes
    """

    def __init__(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
