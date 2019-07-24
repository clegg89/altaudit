#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Functions to get information about a character
"""
from statistics import mean
from .gem_enchant import gem_lookup, enchant_lookup

item_slots = ['head', 'neck', 'shoulder', 'back',
        'chest', 'wrist', 'hands', 'waist',
        'legs', 'feet', 'finger1', 'finger2',
        'trinket1', 'trinket2', 'mainHand', 'offHand']

def get_basic_info(profile, classes, races, realmslug='', region=''):
    mainspec = None
    for spec in profile['talents']:
        if 'selected' in spec and spec['selected']:
            mainspec = spec['spec']['name']

    avatar = profile['thumbnail']
    bust = avatar.replace('avatar', 'inset')
    render = avatar.replace('avatar', 'main')

    return [profile['name'], '{}|{}'.format(profile['realm'],realmslug), region,
            profile['lastModified'], classes[profile['class']],
            profile['level'],
            mainspec,
            'Alliance' if profile['faction'] == 0 else 'Horde' if profile['faction'] == 1 else 'Neutral',
            'Male' if profile['gender'] == 0 else 'Female' if profile['gender'] == 1 else None,
            races[profile['race']]['name'],
            avatar, bust, render]

def _get_item(item_dictionary):
    if item_dictionary:
        return [item_dictionary['itemLevel'],
                item_dictionary['id'],
                item_dictionary['name'],
                item_dictionary['icon'],
                item_dictionary['quality']]
    else:
        return [None, None, None, None, None]

def get_all_items(items_dictionary):
    ilevels = {}
    items = []
    for slot in item_slots:
        ilevels[slot] = items_dictionary[slot]['itemLevel'] if slot in items_dictionary else 0
        items.append(_get_item(items_dictionary[slot]) if slot in items_dictionary else _get_item(None))

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

    for idx,ilvl in enumerate(ilvls):
        if ilvl == 0:
            ilvls[idx] = None

    return [equipped_ilvl] + items

def _get_trait_info(trait, blizzard_api, region='us'):
    if trait is None:
        return None

    spell = blizzard_api.get_spell(region, trait['spellId'])

    return '{}+{}+{}+{}'.format(trait['id'],spell['id'],spell['name'],spell['icon'])

def _get_item_traits(item, character_class, blizzard_api, region='us'):
    if not item['azeriteEmpoweredItem']['azeritePowers']:
        return []

    return blizzard_api.get_item(region, item['id'])['azeriteClassPowers'][str(character_class)]

def _get_azerite_item_info(item, character_class, blizzard_api, region='us'):
    item_traits = item['azeriteEmpoweredItem']['azeritePowers']

    if not item_traits:
        return [[None, None], [None, None], [None, None], [None, None], [None, None]]

    all_traits = _get_item_traits(item, character_class, blizzard_api, region)

    result = [['', ''], ['', ''], ['', ''], ['', ''], ['', '']]

    for trait in all_traits:
        tier = trait['tier']
        trait_info = _get_trait_info(trait, blizzard_api, region)
        result[tier][0] += trait_info + '|'
        if next((t for t in item_traits if t['id'] == trait['id']), None) is not None:
            result[tier][1] = trait_info

    for tier in result:
        tier[0] = tier[0][:-1]

    return result


def get_azerite_info(items_dictionary, character_class, blizzard_api, region='us'):
    result = [None, None, None, None]

    if 'neck' in items_dictionary and items_dictionary['neck']['quality'] == 6:
        result[0] = items_dictionary['neck']['azeriteItem']['azeriteLevel']
        result[1] = items_dictionary['neck']['azeriteItem']['azeriteExperience']
        result[2] = items_dictionary['neck']['azeriteItem']['azeriteExperienceRemaining']

    item_traits = {}
    for slot in ('head', 'shoulder', 'chest'):
        if slot not in items_dictionary:
            item_traits[slot] = [[None, None], [None, None], [None, None], [None, None], [None, None]]
        else:
            item_traits[slot] = _get_azerite_item_info(items_dictionary[slot], character_class, blizzard_api, region)

        result.append(item_traits[slot])

    return result

def _get_item_enchant(item):
    if not item or 'enchant' not in item['tooltipParams']:
        return [None, 0, "None", None]

    enchant_id = item['tooltipParams']['enchant']
    info = enchant_lookup[enchant_id] if enchant_id in enchant_lookup else { 'quality' : 0, 'name' : None, 'description' : None }

    return [enchant_id, info['quality'], info['name'], info['description']]

def _get_hand_enchant(item, faction):
    enchant = _get_item_enchant(item)

    prefix = 'Kul Tiran ' if faction == 0 else 'Zandalari ' if faction == 1 else ''
    if enchant[0] and enchant[2]:
        enchant[2] = prefix + enchant[2]

    return enchant

def get_audit_info(profile, blizzard_api, region='us'):
    result = []

    result.append(_get_item_enchant(profile['items']['mainHand'] if 'mainHand' in profile['items'] else None))

    if 'offHand' not in profile['items'] or 'weaponInfo' not in profile['items']['offHand']:
        result.append([None, None, None, None])
    else:
        result.append(_get_item_enchant(profile['items']['offHand'] if 'offHand' in profile['items'] else None))

    result.append(_get_item_enchant(profile['items']['finger1'] if 'finger1' in profile['items'] else None))
    result.append(_get_item_enchant(profile['items']['finger2'] if 'finger2' in profile['items'] else None))
    result.append(_get_hand_enchant(profile['items']['hands'] if 'hands' in profile['items'] else None, profile['faction']))
    result.append(_get_item_enchant(profile['items']['wrist'] if 'wrist' in profile['items'] else None))
    result.append(profile['audit']['emptySockets'])

    gem_audit = { 'id' : '', 'quality' : '', 'name' : '', 'icon' : '', 'stat' : '', 'slot' : '' }
    for slot in item_slots:
        item = profile['items'][slot] if slot in profile['items'] else None
        if not item:
            continue
        if 'gem0' in item['tooltipParams']:
            gem_audit['slot'] += slot + '|'
            gem_id = item['tooltipParams']['gem0']
            if gem_id in gem_lookup:
                gem_info = gem_lookup[gem_id]
            else:
                api_result = blizzard_api.get_item(region, gem_id, locale='en_US')
                gem_info = { 'quality' : 0, 'name' : api_result['name'], 'icon' : api_result['icon'], 'stat' : api_result['gemInfo']['bonus']['name'] }
            gem_audit['id'] += str(gem_id) + '|'
            gem_audit['quality'] += str(gem_info['quality']) + '|'
            gem_audit['name'] += str(gem_info['name']) + '|'
            gem_audit['icon'] += str(gem_info['icon']) + '|'
            gem_audit['stat'] += str(gem_info['stat']) + '|'

    result.append([gem_audit['id'][:-1],
        gem_audit['quality'][:-1],
        gem_audit['name'][:-1],
        gem_audit['icon'][:-1],
        gem_audit['stat'][:-1],
        gem_audit['slot'][:-1]])

    return result

def get_profession_info(professions_data, faction, region='us'):
    return [["Herbalism", 'trade_herbalism', '150+300'], ['Mining', 'inv_pick_02', '122+300'],
            ["Cooking", 'inv_misc_food_15', '0+300'], ["Fishing", 'trade_fishing', '0+300'], ["Archaeology", 'trade_archaeology', '0+950']]
