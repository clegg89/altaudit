"""Pull Azerite Data from API Response"""

from ..constants import AZERITE_ITEM_SLOTS, AZERITE_TIERS, BLIZZARD_REGION, BLIZZARD_LOCALE
from ..models import AzeriteTrait

def azerite(character, response, db_session, api):
    # TODO make a Item->Trait table so we can avoid always querying the API
    items_response = response['items']

    if 'neck' in items_response and items_response['neck']['quality'] == 6:
        hoa = items_response['neck']['azeriteItem']
        character.hoa_level = hoa['azeriteLevel']
        character.azerite_experience = hoa['azeriteExperience']
        character.azerite_experience_remaining = hoa['azeriteExperienceRemaining']

    for slot in AZERITE_ITEM_SLOTS:
        if slot in items_response:
            _azerite_item(character, response['items'][slot], db_session, api, slot)

def _azerite_item(character, item, db_session, api, slot):
    item_traits = item['azeriteEmpoweredItem']['azeritePowers']

    for tier in range(AZERITE_TIERS):
        setattr(character, '_{}_tier{}_selected'.format(slot, tier), None)
        setattr(character, '_{}_tier{}_available'.format(slot, tier), [])

    if not item_traits:
        for tier in range(AZERITE_TIERS):
            return

    all_traits = _item_traits(item, character.class_id, api)

    for trait in all_traits:
        tier = trait['tier']
        trait_model = _trait(trait, db_session, api)
        getattr(character, '_{}_tier{}_available'.format(slot, tier)).append(trait_model)
        # This will search 'item_traits' for a trait where its id matches this trait's id
        if next((t for t in item_traits if t['id'] == trait['id']), None):
            setattr(character, '_{}_tier{}_selected'.format(slot, tier), trait_model)

def _item_traits(item, class_id, api):
    return api.get_item(BLIZZARD_REGION, item['id'], locale=BLIZZARD_LOCALE)['azeriteClassPowers'][str(class_id)]

def _trait(trait, db_session, api):
    model = db_session.query(AzeriteTrait).filter_by(id=trait['id']).first()

    if not model:
        spell = api.get_spell(BLIZZARD_REGION, trait['spellId'], locale=BLIZZARD_LOCALE)
        model = AzeriteTrait(trait['id'], spell['id'], spell['name'], spell['icon'])

    return model
