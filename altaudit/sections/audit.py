"""Pull Gear Audit Data from API Response"""
import copy

from ..constants import BLIZZARD_REGION, BLIZZARD_LOCALE, ENCHANTED_ITEM_SLOTS, ENCHANT_ITEM_FIELDS, ITEM_SLOTS
from ..models import GemSlotAssociation, Gem
from ..gem_enchant import enchant_lookup

def audit(character, response, db_session, api):
    for slot in ENCHANTED_ITEM_SLOTS:
        _enchant(character, slot, response['items'][slot] if slot in response['items'] else None)

    character.empty_sockets = response['audit']['emptySockets']
    character.gems = []

    for slot in ITEM_SLOTS:
        item = response['items'][slot] if slot in response['items'] else None
        if item and 'gem0' in item['tooltipParams']:
            character.gems.append(GemSlotAssociation(slot, _gem(item, db_session, api)))

def _enchant(character, slot, item):
    # Handle special case of offHand weapon
    if slot == 'offHand' and (not item or 'weaponInfo' not in item):
        for field in ENCHANT_ITEM_FIELDS:
            setattr(character, 'offHand_enchant_{}'.format(field), None)
        return

    if not item or 'enchant' not in item['tooltipParams']:
        setattr(character, '{}_enchant_id'.format(slot), None)
        setattr(character, '{}_enchant_quality'.format(slot), 0)
        setattr(character, '{}_enchant_name'.format(slot), "None")
        setattr(character, '{}_enchant_description'.format(slot), None)
        return

    enchant_id = item['tooltipParams']['enchant']
    info = copy.copy(enchant_lookup[enchant_id]) if enchant_id in enchant_lookup else {'quality' : 0, 'name' : 'None', 'description' : None}

    # Handle special case of hands
    if info['description'] and slot == 'hand':
        f = character.faction_name
        prefix = 'Kul Tiran ' if f == 'alliance' else 'Zandalari 'if f == 'horde' else ''

        info['name'] = prefix + info['name']

    setattr(character, '{}_enchant_id'.format(slot), enchant_id)
    for k,v in info.items():
        setattr(character, '{}_enchant_{}'.format(slot, k), v)

def _gem(item, db_session, api):
    id = item['tooltipParams']['gem0']
    gem_model = db_session.query(Gem).filter_by(id=id).first()

    if not gem_model:
        gem = api.get_item(BLIZZARD_REGION, id, locale=BLIZZARD_LOCALE)
        gem_model = Gem(id, 1, gem['name'], gem['icon'], gem['gemInfo']['bonus']['name'])

    return gem_model
