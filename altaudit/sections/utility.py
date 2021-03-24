"""Utility functions used by multiple sections"""

def is_off_hand_weapon(profile):
    equipped_items = profile['equipment']['equipped_items']
    # Find mainhand if it exists
    mainhand = next((item for item in equipped_items if item['slot']['type'] == 'MAIN_HAND'), None)
    # Special case for fury warriors, only class/spec that can dual-wield two-handed weapons
    try:
        is_fury_warrior = profile['summary']['character_class']['name'] == 'Warrior' and\
            profile['summary']['active_spec']['name'] == 'Fury'
    except KeyError:
        is_fury_warrior = False
    # If mainhand is a two handed weapon (or hunter ranged weapon),
    # set offhand ilvl to main ilvl for equipped ilvl calculation
    if not is_fury_warrior and mainhand and \
            (mainhand['inventory_type']['type'] == 'TWOHWEAPON' or
                    mainhand['item_subclass']['name'] in ('Bow', 'Crossbow', 'Gun')):
        return False
    else:
        return True

def is_primary_enchant_slot(profile, slot):
    if slot not in ['wrist', 'hands', 'feet']:
        return False

    if profile['summary']['character_class']['name'] in ['Mage', 'Priest', 'Warlock']:
        return slot == 'wrist'

    if profile['summary']['character_class']['name'] in ['Demon Hunter', 'Hunter', 'Rogue']:
        return slot == 'feet'

    if profile['summary']['character_class']['name'] in ['Death Knight', 'Warrior']:
        return slot == 'hands'

    if profile['summary']['character_class']['name'] == 'Druid':
        if profile['summary']['active_spec']['name'] in ['Feral', 'Guardian']:
            return slot == 'feet'
        if profile['summary']['active_spec']['name'] in ['Balance', 'Restoration']:
            return slot == 'wrist'

    if profile['summary']['character_class']['name'] == 'Monk':
        if profile['summary']['active_spec']['name'] in ['Brewmaster', 'Windwalker']:
            return slot == 'feet'
        if profile['summary']['active_spec']['name'] == 'Mistweaver':
            return slot == 'wrist'

    if profile['summary']['character_class']['name'] == 'Shaman':
        if profile['summary']['active_spec']['name'] == 'Enhancement':
            return slot == 'feet'
        if profile['summary']['active_spec']['name'] in ['Elemental', 'Restoration']:
            return slot == 'wrist'

    if profile['summary']['character_class']['name'] == 'Paladin':
        if profile['summary']['active_spec']['name'] in ['Protection', 'Retribution']:
            return slot == 'hands'
        if profile['summary']['active_spec']['name'] == 'Holy':
            return slot == 'wrist'

    return False
