#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
Manage Items
"""

class Item:
    def __init__(self, item_dict):
        self.id = item_dict['id']
        self.name = item_dict['name']
        self.icon = item_dict['icon']
        self.quality = item_dict['quality']
        self.ilvl = item_dict['itemLevel']

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.icon == other.icon and self.quality == other.quality and self.ilvl == other.ilvl

    def serialize(self):
        return [self.ilvl, self.id, self.name, self.icon, self.quality]

class ItemManager:
    def __init__(self, items_dict):
        slots = ['head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waist', 'legs', 'feet', 'finger1', 'finger2', 'trinket1', 'trinket2', 'mainHand', 'offHand']

        if 'neck' in items_dict and items_dict['neck']['quality'] == 6:
            self.hoa_level = items_dict['neck']['azeriteItem']['azeriteLevel']
            self.hoa_exp = items_dict['neck']['azeriteItem']['azeriteExperience']
            self.hoa_exp_rem = items_dict['neck']['azeriteItem']['azeriteExperienceRemaining']
        else:
            self.hoa_level = None
            self.hoa_exp = None
            self.hoa_exp_rem = None

        self.items = {}
        for slot in slots:
            if slot in items_dict:
                self.items[slot] = Item(items_dict[slot])

        self.equipped_ilvl = 0
        for item in self.items.values():
            self.equipped_ilvl += item.ilvl

        self.equipped_ilvl /= len(self.items) if len(self.items) > 0 else 1

    def serialize(self):
        ret = [self.hoa_level, self.hoa_exp, self.hoa_exp_rem]
        for item in self.items.values():
            ret.append(item.serialize())

        return ret
