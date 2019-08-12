"""Metadata for the refresh call"""

from ..utility import Utility
from ..constants import VERSION, WOW_PATCH, VALID_RAIDS

def metadata():
    raids = '|'.join(['{}+{}'.format(raid['name'], '_'.join([boss['name'] for boss in raid['encounters']])) for raid in VALID_RAIDS])
    return [Utility.refresh_time, VERSION, WOW_PATCH, raids]
