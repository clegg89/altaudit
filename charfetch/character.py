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
