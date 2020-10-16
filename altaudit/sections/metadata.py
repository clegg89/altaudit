"""Metadata for the refresh call"""

from ..utility import Utility
from ..version import VERSION, WOW_PATCH
from .raids import VALID_RAIDS

def metadata():
    raids = '|'.join(['{}+{}'.format(raid['name'], '_'.join([boss['name'] for boss in raid['encounters']])) for raid in VALID_RAIDS])

    return [Utility.refresh_time, VERSION, WOW_PATCH, raids]
