#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.
"""
Top-Level functions for the module
"""
from wowapi import WowApi

from .utility import load_yaml_file

def fetch_all(tokens_file, character_file):
    tokens = load_yaml_file(tokens_file)
    WowApi(tokens['blizzard']['client_id'], tokens['blizzard']['client_secret'])
