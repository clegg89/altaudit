#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
The Character class
"""

class Character:
    def __init__(self, char_dict, api, classes=None, races=None):
        for k, v in char_dict.items():
            setattr(self, k, v)

        self._classes = classes
        self._races = races

        self.api = api

        self._profile = None

    def _update(self):
        self._profile = self.api.get_character_profile(self.region, self.realm, self.name, locale='en_US', filters='talents,items,statistics,professions,reputation,audit')
        pass

    def _update_if_no_profile(self):
        if not self._profile:
            self._update()

    def get_class(self):
        self._update_if_no_profile()
        if not self._classes:
            self._classes = self.api.get_character_classes('us')

        return self._classes[self._profile['class']]

    def get_race(self):
        self._update_if_no_profile()
        if not self._races:
            self._races = self.api.get_character_races('us')

        return self._races[self._profile['race']]['name']
