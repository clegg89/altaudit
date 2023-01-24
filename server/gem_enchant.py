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
"""
gem_lookup = {
    # Old Gems - Not listed. Quality 1
    # 9.0 Uncommon Gems
    173121 : { 'quality' : 2, 'name' : 'Deadly Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_orange', 'stat' : '+12 Critical Strike' },
    173122 : { 'quality' : 2, 'name' : 'Quick Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_yellow', 'stat' : '+12 Haste' },
    173123 : { 'quality' : 2, 'name' : 'Versatile Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_blue', 'stat' : '+12 Versatility' },
    173124 : { 'quality' : 2, 'name' : 'Masterful Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_purple', 'stat' : '+12 Mastery' },
    173125 : { 'quality' : 2, 'name' : 'Revitalizing Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_red', 'stat' : '+133 health every 10 seconds for each gem socketed' },
    173126 : { 'quality' : 2, 'name' : 'Straddling Jewel Doublet', 'icon' : 'inv_jewelcrafting_90_cutuncommon_green', 'stat' : '+13 speed for each gem socketed' },
    # 9.0 Rare Gems
    173127 : { 'quality' : 3, 'name' : 'Deadly Jewel Cluster', 'icon' : 'inv_jewelcrafting_90_rarecut_orange', 'stat' : '+16 Critical Strike' },
    173128 : { 'quality' : 3, 'name' : 'Quick Jewel Cluster', 'icon' : 'inv_jewelcrafting_90_rarecut_yellow', 'stat' : '+16 Haste' },
    173129 : { 'quality' : 3, 'name' : 'Versatile Jewel Cluster', 'icon' : 'inv_jewelcrafting_90_rarecut_blue', 'stat' : '+16 Versatility' },
    173130 : { 'quality' : 3, 'name' : 'Masterful Jewel Cluster', 'icon' : 'inv_jewelcrafting_90_rarecut_purple', 'stat' : '+16 Mastery' }
    }

"""
There does not seem to be any actual API for looking up enchants by ID. So this is all we have

The name is now provided by the Equipment Profile API, so it is unused. Leaving b/c it helps when reading.
"""
enchant_lookup = {
    # Cloak
    6202 : { 'quality' : 3, 'name' : "Fortified Speed", 'description' : "+20 Stamina and +30 Speed" },
    6203 : { 'quality' : 3, 'name' : "Fortified Avoidance", 'description' : "+20 Stamina and +30 Avoidance" },
    6204 : { 'quality' : 3, 'name' : "Fortified Leech", 'description' : "+20 Stamina and +30 Leech" },
    6208 : { 'quality' : 3, 'name' : "Soul Vitality", 'description' : "+30 Stamina" },

    # Chest
    6216 : { 'quality' : 2, 'name' : "Sacred Stats", 'description' : "+20 Primary Stat" },
    6213 : { 'quality' : 3, 'name' : "Eternal Bulwark", 'description' : "+25 Armor and +20 Strength/Agility" },
    6214 : { 'quality' : 3, 'name' : "Eternal Skirmish", 'description' : "+20 Strength/Agility and Shadow Damage Auto-Attack" },
    6217 : { 'quality' : 3, 'name' : "Eternal Bounds", 'description' : "+20 Intellect and +6% Mana" },
    6230 : { 'quality' : 3, 'name' : "Eternal Stats", 'description' : "+30 Primary Stat" },
    6265 : { 'quality' : 3, 'name' : "Eternal Insight", 'description' : "+20 Intellect and Shadow Damage Spells" },

    # Primary
    ## Wrist
    6219 : { 'quality' : 2, 'name' : "Illuminated Soul", 'description' : "+10 Intellect" },
    6220 : { 'quality' : 3, 'name' : "Eternal Intellect", 'description' : "+15 Intellect" },
    ## Hands
    6209 : { 'quality' : 2, 'name' : "Strength of Soul", 'description' : "+10 Strength" },
    6210 : { 'quality' : 3, 'name' : "Eternal Strength", 'description' : "+15 Strength" },
    ## Feet
    6212 : { 'quality' : 2, 'name' : "Agile Soul", 'description' : "+10 Agility" },
    6211 : { 'quality' : 3, 'name' : "Eternal Agility", 'description' : "+15 Agility" },

    # Ring
    # Bargain
    6163 : { 'quality' : 2, 'name' : "Bargain of Critical Strike", 'description' : "+12 Critical Strike" },
    6165 : { 'quality' : 2, 'name' : "Bargain of Haste", 'description' : "+12 Haste" },
    6167 : { 'quality' : 2, 'name' : "Bargain of Mastery", 'description' : "+12 Mastery" },
    6169 : { 'quality' : 2, 'name' : "Bargain of Versatility", 'description' : "+12 Versatility" },
    # Tenet
    6164 : { 'quality' : 3, 'name' : "Tenet of Critical Strike", 'description' : "+16 Critical Strike" },
    6166 : { 'quality' : 3, 'name' : "Tenet of Haste", 'description' : "+16 Haste" },
    6168 : { 'quality' : 3, 'name' : "Tenet of Mastery", 'description' : "+16 Mastery" },
    6170 : { 'quality' : 3, 'name' : "Tenet of Versatility", 'description' : "+16 Versatility" },

    # Weapons - All Valid
    # Engineering
    6195 : { 'quality' : 3, 'name' : "Infra-green Reflex Sight", 'description' : "Occasionally increase Haste by 303 for 12 sec" },
    6196 : { 'quality' : 3, 'name' : "Optical Target Embiggener", 'description' : "Occasionally increase Critical Strike by 303 for 12 sec" },
    # Enchant
    6223 : { 'quality' : 3, 'name' : "Lightless Force", 'description' : "Chance to send out a wave of Shadow energy, striking 5 enemies" },
    6226 : { 'quality' : 3, 'name' : "Eternal Grace", 'description' : "Sometimes cause a burst of healing on the target of your helpful spells and abilities" },
    6227 : { 'quality' : 3, 'name' : "Ascended Vigor", 'description' : "Sometimes increase your healing received by 12% for 10 sec" },
    6228 : { 'quality' : 3, 'name' : "Sinful Revelation", 'description' : "Your attacks sometimes cause enemies to suffer an additional 6% damage from you for 10 sec" },
    6229 : { 'quality' : 3, 'name' : "Celestial Guidance", 'description' : "Sometimes increase your primary stat by 5%" },

    # DK Runeforges
    3370 : { 'quality' : 4, 'name' : "Rune of the Razorice", 'description' : "Causes extra weapon damage as Frost damage and increases enemies' vulnerability to your Frost attacks by 3%, stacking up to 5 times" },
    3847 : { 'quality' : 4, 'name' : "Rune of the Stoneskin Gargoyle", 'description' : "Increase Armor by 5% and all stats by 5%" },
    3368 : { 'quality' : 4, 'name' : "Rune of the Fallen Crusader", 'description' : "Chance to heal for 6% and increases total Strength by 15% for 15 sec." },
    6241 : { 'quality' : 4, 'name' : "Rune of Sanguination", 'description' : "Cuases Death Strike to deal increased the target's missing health. When you fall below 35% health, you heal for 48% of your maximum health over 8 sec" },
    6242 : { 'quality' : 4, 'name' : "Rune of Spellwarding", 'description' : "Deflect 3% of all spell damage. Taking magic damage has a chance to create a shield that absorbs magic damage equal to 10% of your max health. Damaging the shield causes enemies' cast speed to be reduced by 10% for 6 sec" },
    6243 : { 'quality' : 4, 'name' : "Rune of Hysteria", 'description' : "Increases maximum Runic Power by 20 and attacks have a chance to increase Runic Power generation by 20% for 8 sec" },
    6244 : { 'quality' : 4, 'name' : "Rune of Unending Thirst", 'description' : "Increase movement speed by 5%. Killing an enemy causes you to heal for 5% of your max health and gain 10% Haste and movement speed" },
    6245 : { 'quality' : 4, 'name' : "Rune of the Apocalypse", 'description' : "Your ghoul's attacks have a chance to apply a debuff to the target" }
    }
