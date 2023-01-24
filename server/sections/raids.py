"""Valid Raids"""

"""
Raid Information

Note that raid id is the WCL zone, and the encounter id is the WCL encounter. We use Neither

To find the different difficulty IDs go to Achievement Statistics -> Dungeons & Raids Category
-> Expac Subcategory and find each boss for the reaid there. Wowaudit usually will have this
done before you so its easier to copy.
"""
VALID_RAIDS = [{
  'name' : 'Castle Nathria', 'id' : 26,
  'encounters' : [{
    'id' : 2398, 'name' : 'Shriekwing', 'raid_ids' : {
      'raid_finder' : [14422], 'normal' : [14419], 'heroic' : [14420], 'mythic' : [14421]
    }
  }, {
    'id' : 2418, 'name' : "Huntsman Altimor", 'raid_ids' : {
      'raid_finder' : [14426], 'normal' : [14423], 'heroic' : [14424], 'mythic' : [14425]
    }
  }, {
    'id' : 2383, 'name' : "Hungering Destroyer", 'raid_ids' : {
      'raid_finder' : [14430], 'normal' : [14427], 'heroic' : [14428], 'mythic' : [14429]
    }
  }, {
    'id' : 2402, 'name' : "Sun King's Salvation", 'raid_ids' : {
      'raid_finder' : [14438], 'normal' : [14435], 'heroic' : [14436], 'mythic' : [14437]
    }
  }, {
    'id' : 2405, 'name' : "Artificer Xy'mox", 'raid_ids' : {
      'raid_finder' : [14434], 'normal' : [14431], 'heroic' : [14432], 'mythic' : [14433]
    }
  }, {
    'id' : 2406, 'name' : "Lady Inerva Darkvein", 'raid_ids' : {
      'raid_finder' : [14442], 'normal' : [14439], 'heroic' : [14440], 'mythic' : [14441]
    }
  }, {
    'id' : 2412, 'name' : "The Council of Blood", 'raid_ids' : {
      'raid_finder' : [14446], 'normal' : [14443], 'heroic' : [14444], 'mythic' : [14445]
    }
  }, {
    'id' : 2399, 'name' : "Sludgefist", 'raid_ids' : {
      'raid_finder' : [14450], 'normal' : [14447], 'heroic' : [14448], 'mythic' : [14449]
    }
  }, {
    'id' : 2417, 'name' : "Stone Legion Generals", 'raid_ids' : {
      'raid_finder' : [14454], 'normal' : [14451], 'heroic' : [14452], 'mythic' : [14453]
    }
  }, {
    'id' : 2407, 'name' : "Sire Denathrius", 'raid_ids' : {
      'raid_finder' : [14458], 'normal' : [14455], 'heroic' : [14456], 'mythic' : [14457]
    }
  }]
}]
