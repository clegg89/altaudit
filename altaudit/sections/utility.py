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
    # If mainhand is a two handed weapon, set offhand ilvl to main ilvl for equipped ilvl calculation
    if not is_fury_warrior and mainhand and mainhand['inventory_type']['type'] == 'TWOHWEAPON':
        return False
    else:
        return True
