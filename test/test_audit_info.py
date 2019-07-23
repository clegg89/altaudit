#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
Unit Tests for audit info

Note: These unit tests aren't exhaustive. Only mainHand tests missing enchant and
unrecognized enchant, but all the other slots use the same internal function, so
testing them is moot. As long as that stays the same no further tests are needed
"""

import pytest

import charfetch
from charfetch import get_audit_info

def test_audit_info_mainhand():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'mainHand' : { 'tooltipParams' : { 'enchant' : 6112 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[0] == [6112, 4, "Machinist's Brilliance", "Occasionally increase Intellect by 264 and Mastery, Haste, or Critical Strike by 170 for 15 sec. Your highest stat is always chosen"]

def test_audit_info_mainhand_missing_enchant():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'mainHand' : { 'tooltipParams' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[0] == [None, 0, "None", None]

def test_audit_info_mainhand_unrecognized_enchant():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'mainHand' : { 'tooltipParams' : { 'enchant' : 2231 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[0] == [2231, 0, None, None]

def test_audit_info_offhand():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'offHand' : { 'tooltipParams' : { 'enchant' : 5950 }, 'weaponInfo' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[1] == [5950, 4, "Gale-Force Striking", "Sometimes increase attack speed by 15% for 15 sec. when using melee or ranged attacks and abilities"]

def test_audit_info_offhand_no_enchant_non_weapon():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'offHand' : { 'tooltipParams' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[1] == [None, None, None, None]

def test_audit_info_offhand_no_enchant_weapon():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'offHand' : { 'tooltipParams' : {}, 'weaponInfo' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[1] == [None, 0, "None", None]

def test_audit_info_finger1():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'finger1' : { 'tooltipParams' : { 'enchant' : 5942 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[2] == [5942, 3, "Pact of Critical Strike", "+40 Critical Strike"]

def test_audit_info_finger2():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'finger2' : { 'tooltipParams' : { 'enchant' : 5940 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[3] == [5940, 2, "Seal of Mastery", "+30 Mastery"]

def test_audit_info_hand_horde():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'hands' : { 'tooltipParams' : { 'enchant' : 5937 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[4] == [5937, 4, "Zandalari Crafting", "Increase the speed of crafting items from primary professions on Kul Tiras and Zandalar"]

def test_audit_info_hand_alliance():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 0, 'items' : {
        'hands' : { 'tooltipParams' : { 'enchant' : 5932 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[4] == [5932, 4, "Kul Tiran Herbalism", "Increase the speed of herb gathering on Kul Tiras and Zandalar"]

def test_audit_info_hand_no_enchant():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 0, 'items' : {
        'hands' : { 'tooltipParams' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[4] == [None, 0, "None", None]

def test_audit_info_wrist():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'wrist' : { 'tooltipParams' : { 'enchant' : 5936 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[5] == [5936, 4, "Swift Hearthing", "Increase the speed of your Hearthstone cast while in Kul Tiras or Zandalar"]

@pytest.fixture(params=[0,2,4])
def missing_gems(request):
    return request.param

def test_audit_info_gem_empty_sockets(missing_gems):
    profile = { 'audit' : { 'emptySockets' : missing_gems }, 'faction' : 1, 'items' : {}}

    result = get_audit_info(profile, None, 'us')

    assert result[6] == missing_gems

def test_audit_info_gem_nominal():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'back' : { 'tooltipParams' : { 'gem0' : 153709 }},
        'wrist' : { 'tooltipParams' : { 'gem0' : 168641 }},
        'finger2' : { 'tooltipParams' : { 'gem0' : 154127 }}}}

    result = get_audit_info(profile, None, 'us')

    assert result[7] == ['153709|168641|154127', '4|5|3', "Kraken's Eye of Intellect|Quick Sand Spinel|Quick Owlseye", "inv_jewelcrafting_80_specialgemcut01|inv_misc_gem_x4_uncommon_perfectcut_yellow|inv_jewelcrafting_80_cutgem02_yellow", "+80 Intellect|+50 Haste|+40 Haste", "back|wrist|finger2"]

def test_audit_info_no_gems():
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'averageItemLevel' : 380,
        'back' : { 'tooltipParams' : {}},
        'wrist' : { 'tooltipParams' : {}},
        'finger2' : { 'tooltipParams' : {}}}}

    result = get_audit_info(profile, None, 'us')

    assert result[7] == ['', '', '', '', '', '']

def test_audit_info_unkown_gem_call_api(mock_api):
    profile = { 'audit' : { 'emptySockets' : 0 }, 'faction' : 1, 'items' : {
        'finger2' : { 'tooltipParams' : { 'gem0' : 151584 }}}}

    mock_api.get_item.return_value = { 'name' : "Masterful Argulite", 'icon' : "inv_jewelcrafting_argusgemcut_purple_miscicons", 'gemInfo' : { 'bonus' : { 'name' : "+11 Mastery" }}}

    result = get_audit_info(profile, mock_api, 'us')

    assert len(mock_api.method_calls) == 1
    mock_api.get_item.assert_called_once_with('us', 151584, locale='en_US')
    assert result[7] == ['151584', '0', "Masterful Argulite", "inv_jewelcrafting_argusgemcut_purple_miscicons", "+11 Mastery", "finger2"]
