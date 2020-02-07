"""Pull Item Data from API Response"""

from statistics import mean

from ..constants import ITEM_SLOTS, ITEM_FIELDS

def items(character, response, db_session, api):
    items_response = response['items']
    ilevels = {}

    for slot in ITEM_SLOTS:
        ilevels[slot] = items_response[slot]['itemLevel'] if slot in items_response else 0
        _item(character, slot, items_response[slot] if slot in items_response else None)

    # Special case for missing offHand
    # Note: This is not technically correct. Blizzard will only replace
    # the offHand slot if the mainHand slot is a 2h weapon.
    # However, we don't have enough information from the character item
    # list to determine this. We could query the Item API and use the
    # class/subclass to determine if it is 1h/2h, but that's a lot of
    # extra work, for very little reward. We'll mark it as a todo
    # TODO Query wow API to determine if mainHand is 1h or 2h
    if ilevels['offHand'] == 0:
        ilevels['offHand'] = ilevels['mainHand']

    ilvls = list(ilevels.values())

    equipped_ilvl = mean(ilvls)

    ilvls = [ilvl if ilvl != 0 else None for ilvl in ilvls]

    character.estimated_ilvl = equipped_ilvl

def _item(character, slot, item_response):
    for field in ['itemLevel', 'id', 'name', 'icon', 'quality']:
        setattr(character, '{}_{}'.format(slot, field), item_response[field] if item_response else None)
