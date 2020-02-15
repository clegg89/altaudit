"""Pull Item Data from API Response"""

from statistics import mean

from ..models import ITEM_SLOTS

def items(character, profile, db_session, api):
    equipped_items = profile['equipment']['equipped_items']
    ilevels = {slot : 0 for slot in ITEM_SLOTS}

    for item in equipped_items:
        slot = item['slot']['type'].lower()
        ilevels[slot] = item['level']['value']
        _item(character, slot, item)

    if ilevels['off_hand'] == 0:
        # Find mainhand if it exists
        mainhand = next(iter([item for item in equipped_items if item['slot']['type'] == 'MAIN_HAND']), None)
        # If mainhand is a two handed weapon, set offhand ilvl to main ilvl for equipped ilvl calculation
        if mainhand and mainhand['inventory_type']['type'] == 'TWOHWEAPON':
            ilevels['off_hand'] = ilevels['main_hand']
        else:
            ilevels['off_hand'] = 0

    equipped_ilvl = mean(list(ilevels.values()))

    character.estimated_ilvl = equipped_ilvl

def _item(character, slot, item):
    setattr(character, '{}_itemLevel'.format(slot), item['level']['value'])
    setattr(character, '{}_id'.format(slot), item['item']['id'])
    setattr(character, '{}_name'.format(slot), item['name'])
    setattr(character, '{}_quality'.format(slot), item['quality']['name'])
