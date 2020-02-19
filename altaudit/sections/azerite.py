"""Pull Azerite Data from API Response"""

from ..blizzard import BLIZZARD_REGION, BLIZZARD_LOCALE
from ..models import AzeriteTrait, AZERITE_ITEM_SLOTS, AZERITE_TIERS

def azerite(character, response, db_session, api):
    # TODO make a Item->Trait table so we can avoid always querying the API
    equipment = response['equipment']['equipped_items']

    neck = next((item for item in equipment if item['slot']['type'] == 'NECK'), None)

    if neck and neck['name'] == 'Heart of Azeroth':
        character.hoa_level = neck['azerite_details']['level']['value']
        character.azerite_percentage = neck['azerite_details']['percentage_to_next_level']

    for slot in AZERITE_ITEM_SLOTS:
        azerite_item = next((item for item in equipment if item['slot']['type'].lower() == slot), None)
        if azerite_item and 'azerite_details' in azerite_item:
            _azerite_item(character, azerite_item, db_session, api)

def _azerite_item(character, item, db_session, api):
    slot = item['slot']['type'].lower()
    item_traits = item['azerite_details']['selected_powers']

    for tier in range(AZERITE_TIERS):
        setattr(character, '_{}_tier{}_selected'.format(slot, tier), None)
        setattr(character, '_{}_tier{}_available'.format(slot, tier), [])

    all_traits = _item_traits(item, character, api)

    if all_traits:
        for trait in all_traits:
            tier = trait['tier']
            trait_model = _trait(trait, db_session, api)
            getattr(character, '_{}_tier{}_available'.format(slot, tier)).append(trait_model)
            # This will search 'item_traits' for a trait where its id matches this trait's id
            if next((t for t in item_traits if t['id'] == trait['id']), None):
                setattr(character, '_{}_tier{}_selected'.format(slot, tier), trait_model)

def _item_traits(item, character, api):
    return next((traits['powers'] for traits in api.get_data_resource('{}&locale={}'.format(item['item']['key']['href'], BLIZZARD_LOCALE), BLIZZARD_REGION)['azerite_class_powers'] if traits['playable_class']['name'] == character.class_name), None)

def _trait(trait, db_session, api):
    model = db_session.query(AzeriteTrait).filter_by(id=trait['id']).first()

    if not model:
        # Spell API not working
        # This is only useful to get the icon
        # spell = api.get_data_resource('{}&locale={}'.format(trait['spell']['key']['href'], BLIZZARD_LOCALE), BLIZZARD_REGION)
        model = AzeriteTrait(trait['id'], trait['spell']['id'], trait['spell']['name'], None)

    return model
