#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
Unit Tests for audit info
"""

import pytest

from charfetch import get_audit_info

def test_audit_info_weapon(mock_api):
    profile = {'faction' : 1, 'items' : {
        'mainHand' : { 'tooltipParams' : { 'enchant' : 6112 }}}}

    result = get_audit_info(profile, mock_api, 'us')

    assert mock_api.method_calls == []
    assert result[0] == [6112, 4, "Machinist's Brilliance", "Occasionally increase Intellect by 264 and Mastery, Haste, or Critical Strike by 170 for 15 sec. Your highest stat is always chosen"]
