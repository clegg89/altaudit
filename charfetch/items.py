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

    def serialize(self):
        return [self.ilvl, self.id, self.name, self.icon, self.quality]

class ItemManager:
    def __init__(self, items_dict):
        if 'neck' in items_dict and items_dict['neck']['quality'] == 6:
            self.hoa_level = items_dict['neck']['azeriteItem']['azeriteLevel']
            self.hoa_exp = items_dict['neck']['azeriteItem']['azeriteExperience']
            self.hoa_exp_rem = items_dict['neck']['azeriteItem']['azeriteExperienceRemaining']
        else:
            self.hoa_level = ''
            self.hoa_exp = ''
            self.hoa_exp_rem = ''
