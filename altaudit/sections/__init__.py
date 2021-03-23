from . import basic
from . import items
from . import audit
from . import professions
from . import reputations
from . import pve
from .raiderio import raiderio
from .metadata import metadata

sections = [
        basic.basic,
        items.items,
        audit.audit,
        # professions, Not yet available in Profile API
        reputations.reputations,
        pve.pve ]
