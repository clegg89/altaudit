"""Pull Azerite Data from API Response"""

from wowapi import WowApiException

from ..blizzard import BLIZZARD_REGION, BLIZZARD_LOCALE
from ..models import AzeriteTrait, AZERITE_ITEM_SLOTS, AZERITE_TIERS

def azerite(character, profile, db_session, api):
    """
    Azerite item information. Default to not failing on
    anything except equipped_items not being present
    """
    # TODO make a Item->Trait table so we can avoid always querying the API
    equipment = profile['equipment']['equipped_items']

    neck = next((item for item in equipment if item['slot']['type'] == 'NECK'), None)

    if neck and neck['name'] == 'Heart of Azeroth':
        try:
            character.hoa_level = neck['azerite_details']['level']['value']
            character.azerite_percentage = neck['azerite_details']['percentage_to_next_level']
        except KeyError:
            character.hoa_level = None
            character.azerite_percentage = None

    for slot in AZERITE_ITEM_SLOTS:
        azerite_item = next((item for item in equipment if item['slot']['type'].lower() == slot), None)
        if azerite_item and 'azerite_details' in azerite_item:
            _azerite_item(character, azerite_item, db_session, api)

def _azerite_item(character, item, db_session, api):
    slot = item['slot']['type'].lower()

    for tier in range(AZERITE_TIERS):
        setattr(character, '_{}_tier{}_selected'.format(slot, tier), None)
        setattr(character, '_{}_tier{}_available'.format(slot, tier), [])

    try:
        item_traits = item['azerite_details']['selected_powers']
    except (KeyError, TypeError):
        item_traits = None

    all_traits = _get_all_traits(item, character, api)

    _action_per_trait(item_traits, db_session,
            lambda trait: trait['spell_tooltip']['spell'],
            lambda tier, model: setattr(character, '_{}_tier{}_selected'.format(slot, tier), model))

    _action_per_trait(all_traits, db_session,
            lambda trait: trait['spell'],
            lambda tier, model: getattr(character, '_{}_tier{}_available'.format(slot, tier)).append(model))

def _get_all_traits(item, character, api):
    try:
        return next((traits['powers'] for traits in api.get_data_resource('{}&locale={}'.format(item['item']['key']['href'], BLIZZARD_LOCALE), BLIZZARD_REGION)['azerite_class_powers'] if traits['playable_class']['name'] == character.class_name), None)
    except (KeyError, WowApiException):
        return None

def _action_per_trait(traits, db_session, spell_lookup, action):
    if traits:
        for trait in traits:
            if trait and 'tier' in trait:
                tier = trait['tier']
                trait_model = _trait(trait, db_session, spell_lookup)
                action(tier, trait_model)

def _trait(trait, db_session, spell_lookup):
    try:
        model = db_session.query(AzeriteTrait).filter_by(id=trait['id']).first()

        if not model:
            # Spell API not working
            # This is only useful to get the icon
            # spell = api.get_data_resource('{}&locale={}'.format(trait['spell']['key']['href'], BLIZZARD_LOCALE), BLIZZARD_REGION)
            spell = spell_lookup(trait)
            model = AzeriteTrait(trait['id'], spell['id'], spell['name'], None)

        return model

    except KeyError:
        return None
