"""Pull Item Data from API Response"""

from statistics import mean
import re

from ..models import ITEM_SLOTS
from .utility import is_off_hand_weapon

def items(character, profile, db_session, api):
    """
    Get basic item info. If equipped_items is missing, just fail.
    I don't think there would be any reasonable case where that would happen
    """
    equipped_items = profile['equipment']['equipped_items']
    ilevels = {slot : 0 for slot in ITEM_SLOTS}

    for item in equipped_items:
        slot = item['slot']['type'].lower()
        try:
            if slot in ITEM_SLOTS:
                ilevels[slot] = item['level']['value']
        except KeyError:
            ilevels[slot] = 0
        _item(character, slot, item)

    if ilevels['off_hand'] == 0 and not is_off_hand_weapon(profile):
        ilevels['off_hand'] = ilevels['main_hand']

    equipped_ilvl = mean(list(ilevels.values()))

    character.estimated_ilvl = equipped_ilvl

    # Bolt on cloak data here
    cloak = next((item for item in equipped_items if item['slot']['type'] == 'BACK'), None)
    if cloak and cloak['name'] == "Ashjra'kamas, Shroud of Resolve":
        try:
            character.cloak_rank = int(re.match(r'Rank ([0-9]+)', cloak['name_description']['display_string']).group(1))
        except (KeyError,TypeError):
            pass

def _item(character, slot, item):
    try:
        setattr(character, '{}_itemLevel'.format(slot), item['level']['value'])
    except KeyError:
        setattr(character, '{}_itemLevel'.format(slot), None)
    try:
        setattr(character, '{}_id'.format(slot), item['item']['id'])
    except KeyError:
        setattr(character, '{}_id'.format(slot), None)
    try:
        setattr(character, '{}_name'.format(slot), item['name'])
    except KeyError:
        setattr(character, '{}_name'.format(slot), None)
    try:
        setattr(character, '{}_quality'.format(slot), item['quality']['name'])
    except KeyError:
        setattr(character, '{}_quality'.format(slot), None)
