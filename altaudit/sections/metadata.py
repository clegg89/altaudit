"""Metadata for the refresh call"""

from ..utility import Utility
from ..constants import VERSION, WOW_PATCH

def metadata():
    return [Utility.refresh_time, VERSION, WOW_PATCH]
