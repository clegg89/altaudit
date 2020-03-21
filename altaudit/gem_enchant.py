#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Gem and Enchant Lookup Tables
"""

"""
To save some API calls we're going to keep this data here. It'll cover most gems.
Eventually we may to want to legitimately cache gem data in a database.
"""
gem_lookup = {
    # Old Gems - Not listed. Quality 1
    # Uncommon Gems
    153710 : { 'quality' : 2, 'name' : 'Deadly Solstone', 'icon' : 'inv_jewelcrafting_80_cutgem01_orange', 'stat' : '+30 Critical Strike' },
    153711 : { 'quality' : 2, 'name' : 'Quick Golden Beryl', 'icon' : 'inv_jewelcrafting_80_cutgem01_yellow', 'stat' : '+30 Haste' },
    153712 : { 'quality' : 2, 'name' : 'Versatile Kyanite', 'icon' : 'inv_jewelcrafting_80_cutgem01_blue', 'stat' : '+30 Versatility' },
    153713 : { 'quality' : 2, 'name' : 'Masterful Kubline', 'icon' : 'inv_jewelcrafting_80_cutgem01_purple', 'stat' : '+30 Mastery' },
    153714 : { 'quality' : 2, 'name' : 'Insightful Rubellite', 'icon' : 'inv_jewelcrafting_80_cutgem01_red', 'stat' : '+5% Experience' },
    153715 : { 'quality' : 2, 'name' : 'Straddling Viridium', 'icon' : 'inv_jewelcrafting_80_cutgem01_green', 'stat' : '+3% Movement Speed' },
    # Rare Gems
    154126 : { 'quality' : 3, 'name' : 'Deadly Amberblaze', 'icon' : 'inv_jewelcrafting_80_cutgem02_orange', 'stat' : '+40 Critical Strike' },
    154127 : { 'quality' : 3, 'name' : 'Quick Owlseye', 'icon' : 'inv_jewelcrafting_80_cutgem02_yellow', 'stat' : '+40 Haste' },
    154128 : { 'quality' : 3, 'name' : 'Versatile Royal Quartz', 'icon' : 'inv_jewelcrafting_80_cutgem02_blue', 'stat' : '+40 Versatility' },
    154129 : { 'quality' : 3, 'name' : 'Masterful Tidal Amethyst', 'icon' : 'inv_jewelcrafting_80_cutgem02_purple', 'stat' : '+40 Mastery' },
    169220 : { 'quality' : 3, 'name' : 'Straddling Sage Agate', 'icon' : 'inv_misc_gem_x4_uncommon_perfectcut_green', 'stat' : '+5% Movement Speed' },
    # 8.0 Unique Epic Gems
    153707 : { 'quality' : 4, 'name' : "Kraken's Eye of Strength", 'icon' : 'inv_jewelcrafting_80_specialgemcut01', 'stat' : '+80 Strength' },
    153708 : { 'quality' : 4, 'name' : "Kraken's Eye of Agility", 'icon' : 'inv_jewelcrafting_80_specialgemcut01', 'stat' : '+80 Agility' },
    153709 : { 'quality' : 4, 'name' : "Kraken's Eye of Intellect", 'icon' : 'inv_jewelcrafting_80_specialgemcut01', 'stat' : '+80 Intellect' },
    # Epic Gems
    168639 : { 'quality' : 5, 'name' : 'Deadly Lava Lazuli', 'icon' : 'inv_misc_gem_x4_uncommon_perfectcut_orange', 'stat' : '+50 Critical Strike' },
    168640 : { 'quality' : 5, 'name' : 'Masterful Sea Current', 'icon' : 'inv_misc_gem_x4_uncommon_perfectcut_purple', 'stat' : '+50 Mastery' },
    168641 : { 'quality' : 5, 'name' : 'Quick Sand Spinel', 'icon' : 'inv_misc_gem_x4_uncommon_perfectcut_yellow', 'stat' : '+50 Haste' },
    168642 : { 'quality' : 5, 'name' : 'Versatile Dark Opal', 'icon' : 'inv_misc_gem_x4_uncommon_perfectcut_blue', 'stat' : '+50 Versatility' },
    # 8.2 Unique Epic Gems
    168636 : { 'quality' : 6, 'name' : "Leviathan's Eye of Strength", 'icon' : 'inv_misc_metagem_b', 'stat' : '+120 Strength' },
    168637 : { 'quality' : 6, 'name' : "Leviathan's Eye of Agility", 'icon' : 'inv_misc_metagem_b', 'stat' : '+120 Agility' },
    168638 : { 'quality' : 6, 'name' : "Leviathan's Eye of Intellect", 'icon' : 'inv_misc_metagem_b', 'stat' : '+120 Intellect' }}

"""
There does not seem to be any actual API for looking up enchants by ID. So this is all we have

The name is now provided by the Equipment Profile API, so it is unused. Leaving b/c it helps when reading.
"""
enchant_lookup = {
    # Ring
    # Pact
    5938 : { 'quality' : 2, 'name' : "Seal of Critical Strike", 'description' : "+30 Critical Strike" },
    5939 : { 'quality' : 2, 'name' : "Seal of Haste", 'description' : "+30 Haste" },
    5940 : { 'quality' : 2, 'name' : "Seal of Mastery", 'description' : "+30 Mastery" },
    5941 : { 'quality' : 2, 'name' : "Seal of Versatility", 'description' : "+30 Versatility" },
    # Seal
    5942 : { 'quality' : 3, 'name' : "Pact of Critical Strike", 'description' : "+40 Critical Strike" },
    5943 : { 'quality' : 3, 'name' : "Pact of Haste", 'description' : "+40 Haste" },
    5944 : { 'quality' : 3, 'name' : "Pact of Mastery", 'description' : "+40 Mastery" },
    5945 : { 'quality' : 3, 'name' : "Pact of Versatility", 'description' : "+40 Versatility" },
    # Accord
    6108 : { 'quality' : 4, 'name' : "Accord of Critical Strike", 'description' : "+60 Critical Strike" },
    6109 : { 'quality' : 4, 'name' : "Accord of Haste", 'description' : "+60 Haste" },
    6110 : { 'quality' : 4, 'name' : "Accord of Mastery", 'description' : "+60 Mastery" },
    6111 : { 'quality' : 4, 'name' : "Accord of Versatilty", 'description' : "+60 Versatility" },

    # Weapons - All Valid
    # Enchant
    5946 : { 'quality' : 4, 'name' : "Coastal Surge", 'description' : "Sometimes cause helpful spells to put a short heal over time effect on the target for 10 sec." },
    5948 : { 'quality' : 4, 'name' : "Siphoning", 'description' : "Increase Leech by 100" },
    5949 : { 'quality' : 4, 'name' : "Torrent of Elements", 'description' : "Sometimes increase elemental spell damage by 10%" },
    5950 : { 'quality' : 4, 'name' : "Gale-Force Striking", 'description' : "Sometimes increase attack speed by 15% for 15 sec. when using melee or ranged attacks and abilities" },
    5962 : { 'quality' : 4, 'name' : "Versatile Navigation", 'description' : "Sometimes increase Versatility by 50 for 30 sec., stacking up to 5 times. Upon reaching 5 stacks, all stacks are consumed to grant you 600 Versatility for 10 sec." },
    5963 : { 'quality' : 4, 'name' : "Quick Navigation", 'description' : "Sometimes increase Haste by 50 for 30 sec., stacking up to 5 times. Upon reaching 5 stacks, all stacks are consumed to grant you 600 Haste for 10 sec." },
    5964 : { 'quality' : 4, 'name' : "Masterful Navigation", 'description' : "Sometimes increase Mastery by 50 for 30 sec., stacking up to 5 times. Upon reaching 5 stacks, all stacks are consumed to grant you 600 Mastery for 10 sec." },
    5965 : { 'quality' : 4, 'name' : "Deadly Navigation", 'description' : "Sometimes increase Critical Strike by 50 for 30 sec., stacking up to 5 times. Upon reaching 5 stacks, all stacks are consumed to grant you 600 Critical Strike for 10 sec." },
    5966 : { 'quality' : 4, 'name' : "Stalwart Navigation", 'description' : "Sometimes increase Armor by 50 for 30 sec., stacking up to 5 times. Upon reaching 5 stacks, all stacks are consumed to grant you 600 Armor for 10 sec." },
    6148 : { 'quality' : 4, 'name' : "Force Multiplier", 'description' : "Occasionally increase Strength or Agility by 264 and Mastery, Haste, or Critical Strike by 170 for 15 sec. Your highest stat is always chosen" },
    6112 : { 'quality' : 4, 'name' : "Machinist's Brilliance", 'description' : "Occasionally increase Intellect by 264 and Mastery, Haste, or Critical Strike by 170 for 15 sec. Your highest stat is always chosen" },
    6150 : { 'quality' : 4, 'name' : "Naga Hide", 'description' : "When you Block, Dodge, or Parry, you have a chance to increase Strength or Agility by 264 for 15 sec. When active, absorb 15,000 damage" },
    6149 : { 'quality' : 4, 'name' : "Oceanic Restoration", 'description' : "Occasionally increase Intellect by 264 for 15 sec., and restore 400 mana" },

    # DK Runeforges
    3847 : { 'quality' : 4, 'name' : "Rune of the Stoneskin Gargoyle", 'description' : "Increase Armor by 5% and all stats by 5%" },
    3368 : { 'quality' : 4, 'name' : "Rune of the Fallen Crusader", 'description' : "Chance to heal for 6% and increases total Strength by 15% for 15 sec." },
    3370 : { 'quality' : 4, 'name' : "Rune of the Razorice", 'description' : "Causes 74% extra weapon damage as Frost damage and increases enemies' vulnerability to your Frost attacks by 3%, stacking up to 5 times" },

    # Wrist
    5936 : { 'quality' : 4, 'name' : "Swift Hearthing",  'description' : "Increase the speed of your Hearthstone cast while in Kul Tiras or Zandalar" },
    5970 : { 'quality' : 4, 'name' : "Safe Hearthing", 'description' : "Create an absorb shield around you while using your Hearthstone on Kul Tiras or Zandalar" },
    5971 : { 'quality' : 4, 'name' : "Cooled Hearthing", 'description' : "Reduce the cooldown of your Hearthstone by 5 minutes while in Kul Tiras or Zandalar" },

    # Gloves
    5932 : { 'quality' : 4, 'name' : "Herbalism", 'description' : "Increase the speed of herb gathering on Kul Tiras and Zandalar" },
    5933 : { 'quality' : 4, 'name' : "Mining", 'description' : "Increase the speed of mining on Kul Tiras and Zandalar" },
    5934 : { 'quality' : 4, 'name' : "Skinning", 'description' : "Increase the speed of skinning on Kul Tiras and Zandalar" },
    5935 : { 'quality' : 4, 'name' : "Surveying", 'description' : "Increase the speed of archaeological surveying on Kul Tiras and Zandalar" },
    5937 : { 'quality' : 4, 'name' : "Crafting", 'description' : "Increase the speed of crafting items from primary professions on Kul Tiras and Zandalar" }}
