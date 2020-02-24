"""Pull Gear Audit Data from API Response"""
import re

from ..blizzard import BLIZZARD_REGION, BLIZZARD_LOCALE
from ..models import GemSlotAssociation, Gem, ITEM_SLOTS, ENCHANTED_ITEM_SLOTS, ENCHANT_ITEM_FIELD_COLUMNS
from ..gem_enchant import enchant_lookup
from .utility import is_off_hand_weapon

"Item Enchant Fields"
ENCHANT_ITEM_FIELDS = [field[0] for field in ENCHANT_ITEM_FIELD_COLUMNS]

def audit(character, profile, db_session, api):
    equipped_items = profile['equipment']['equipped_items']

    character.empty_sockets = 0
    character.gems = []

    for slot in ENCHANTED_ITEM_SLOTS:
        setattr(character, '{}_enchant_id'.format(slot), None)
        setattr(character, '{}_enchant_quality'.format(slot), 0)
        setattr(character, '{}_enchant_name'.format(slot), "None")
        setattr(character, '{}_enchant_description'.format(slot), None)

    for item in equipped_items:
        if 'sockets' in item:
            for socket in item['sockets']:
                if 'item' not in socket:
                    character.empty_sockets += 1
                    # Here is where we would note the slot of the item
                else:
                    character.gems.append(GemSlotAssociation(item['slot']['type'].lower(), _gem(socket, db_session)))
        if item['slot']['type'].lower() in ENCHANTED_ITEM_SLOTS:
            _enchant(character, item)

    # Final corner case for off hand. Similiar to item audit, we only
    # ignore missing offhands if the main hand weapon is two handed
    offhand = next((item for item in equipped_items if item['slot']['type'] == 'OFF_HAND'), None)
    if not offhand and not is_off_hand_weapon(profile):
        for field in ENCHANT_ITEM_FIELDS:
            setattr(character, 'off_hand_enchant_{}'.format(field), None)

def _enchant(character, item):
    slot = item['slot']['type'].lower()

    # Handle special case of offHand weapon (this will trigger if the item is not a weapon)
    if slot == 'off_hand' and item['inventory_type']['type'] != 'WEAPON':
        for field in ENCHANT_ITEM_FIELDS:
            setattr(character, 'off_hand_enchant_{}'.format(field), None)
        return

    if 'enchantments' not in item:
        setattr(character, '{}_enchant_id'.format(slot), None)
        setattr(character, '{}_enchant_quality'.format(slot), 0)
        setattr(character, '{}_enchant_name'.format(slot), "None")
        setattr(character, '{}_enchant_description'.format(slot), None)
        return

    # I don't know of any case where there's more than 1 enchant, and our database isn't set up for it
    # anyway. So just grab the first enchant.
    enchant = item['enchantments'][0]
    enchant_id = enchant['enchantment_id']
    if 'source_item' in enchant:
        name = re.sub("Enchant [a-zA-Z]+ - ", "", enchant['source_item']['name'])
    else:
        name = re.sub("Enchanted: ", "", enchant['display_string'])

    setattr(character, '{}_enchant_id'.format(slot), enchant_id)
    setattr(character, '{}_enchant_name'.format(slot), name)

    # TODO Description is now available on the API (sort of), maybe query for it?
    # Could treat like gems and create a table for it
    if enchant_id in enchant_lookup:
        setattr(character, '{}_enchant_quality'.format(slot), enchant_lookup[enchant_id]['quality'])
        setattr(character, '{}_enchant_description'.format(slot), enchant_lookup[enchant_id]['description'])

def _gem(socket, db_session):
    id = socket['item']['id']
    gem_model = db_session.query(Gem).filter_by(id=id).first()

    if not gem_model:
        # If it is not in database, the quality is 1. New API makes getting icon a pain, so ignore
        gem_model = Gem(id, 1, socket['item']['name'], None, socket['display_string'])

    return gem_model
