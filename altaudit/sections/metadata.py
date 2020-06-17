"""Metadata for the refresh call"""

from ..utility import Utility
from ..version import VERSION, WOW_PATCH
from .raids import VALID_RAIDS

def metadata(region):
    raids = '|'.join(['{}+{}'.format(raid['name'], '_'.join([boss['name'] for boss in raid['encounters']])) for raid in VALID_RAIDS])

    max_corruption_resist = 0

    if Utility.year[region] > 2020:
        max_corruption_resist = 125

    max_corruption_resist = ((Utility.week[region] - 12) * 3) + 50

    if max_corruption_resist > 125:
        max_corruption_resist = 125

    return [Utility.refresh_time, VERSION, WOW_PATCH, raids, max_corruption_resist]
