"""Valid Raids"""

"""
Raid Information

Note that raid id is the WCL zone, and the encounter id is the WCL encounter. We use Neither
"""
VALID_RAIDS = [{
  'name' : 'Uldir', 'id' : 19,
  'encounters' : [{
    'id' : 2144, 'name' : 'Taloc', 'raid_ids' : {
      'raid_finder' : [12786], 'normal' : [12787], 'heroic' : [12788], 'mythic' : [12789]
    }
  }, {
    'id' : 2141, 'name' : 'MOTHER', 'raid_ids' : {
      'raid_finder' : [12790], 'normal' : [12791], 'heroic' : [12792], 'mythic' : [12793]
    }
  }, {
    'id' : 2128, 'name' : 'Fetid Devourer', 'raid_ids' : {
      'raid_finder' : [12794], 'normal' : [12795], 'heroic' : [12796], 'mythic' : [12797]
    }
  }, {
    'id' : 2136, 'name' : "Zek'voz, Herald of N'zoth", 'raid_ids' : {
      'raid_finder' : [12798], 'normal' : [12799], 'heroic' : [12800], 'mythic' : [12801]
    }
  }, {
    'id' : 2134, 'name' : 'Vectis', 'raid_ids' : {
      'raid_finder' : [12802], 'normal' : [12803], 'heroic' : [12804], 'mythic' : [12805]
    }
  }, {
    'id' : 2145, 'name' : 'Zul, Reborn', 'raid_ids' : {
      'raid_finder' : [12808], 'normal' : [12809], 'heroic' : [12810], 'mythic' : [12811]
    }
  }, {
    'id' : 2135, 'name' : 'Mythrax the Unraveler', 'raid_ids' : {
      'raid_finder' : [12813], 'normal' : [12814], 'heroic' : [12815], 'mythic' : [12816]
    }
  }, {
    'id' : 2122, 'name' : "G'huun", 'raid_ids' : {
      'raid_finder' : [12817], 'normal' : [12818], 'heroic' : [12819], 'mythic' : [12820]
    }
  }]
}, {
  'name' : "Battle of Dazar'alor", 'id' : 21,
  'encounters' : [{
    'id' : 2265, 'name' : 'Champion of the Light', 'raid_ids' : {
      'raid_finder' : [13328], 'normal' : [13329], 'heroic' : [13330], 'mythic' : [13331]
    }
  }, {
    'id' : 2263, 'name' : 'Grong', 'raid_ids' : {
      'raid_finder' : [13332, 13344], 'normal' : [13333, 13346], 'heroic' : [13334, 13347], 'mythic' : [13336, 13348]
    }
  }, {
    'id' : 2266, 'name' : 'Jadefire Masters', 'raid_ids' : {
      'raid_finder' : [13354, 13349], 'normal' : [13355, 13350], 'heroic' : [13356, 13351], 'mythic' : [13357, 13353]
    }
  }, {
    'id' : 2271, 'name' : 'Opulence', 'raid_ids' : {
      'raid_finder' : [13358], 'normal' : [13359], 'heroic' : [13361], 'mythic' : [13362]
    }
  }, {
    'id' : 2268, 'name' : 'Conclave of the Chosen', 'raid_ids' : {
      'raid_finder' : [13363], 'normal' : [13364], 'heroic' : [13365], 'mythic' : [13366]
    }
  }, {
    'id' : 2272, 'name' : 'King Rastakhan', 'raid_ids' : {
      'raid_finder' : [13367], 'normal' : [13368], 'heroic' : [13369], 'mythic' : [13370]
    }
  }, {
    'id' : 2276, 'name' : 'Mekkatorque', 'raid_ids' : {
      'raid_finder' : [13371], 'normal' : [13372], 'heroic' : [13373], 'mythic' : [13374]
    }
  }, {
    'id' : 2280, 'name' : 'Stormwall Blockade', 'raid_ids' : {
      'raid_finder' : [13375], 'normal' : [13376], 'heroic' : [13377], 'mythic' : [13378]
    }
  }, {
    'id' : 2281, 'name' : 'Lady Jaina Proudmoore', 'raid_ids' : {
      'raid_finder' : [13379], 'normal' : [13380], 'heroic' : [13381], 'mythic' : [13382]
    }
  }]
}, {
  'name' : 'Crucible of Storms', 'id' : 22,
  'encounters' : [{
    'id' : 2269, 'name' : 'The Restless Cabal', 'raid_ids' : {
      'raid_finder' : [13404], 'normal' : [13405], 'heroic' : [13406], 'mythic' : [13407]
    }
  }, {
    'id' : 2273, 'name' : "Uu'nat, Harbinger of the Void", 'raid_ids' : {
      'raid_finder' : [13408], 'normal' : [13411], 'heroic' : [13412], 'mythic' : [13413]
    }
  }]
}, {
  'name' : 'The Eternal Palace', 'id' : 23,
  'encounters' : [{
    'id' : 2298, 'name' : 'Abyssal Commander Sivara', 'raid_ids' : {
      'raid_finder' : [13587], 'normal' : [13588], 'heroic' : [13589], 'mythic' : [13590]
    }
  }, {
    'id' : 2305, 'name' : "Radiance of Azshara", 'raid_ids' : {
      'raid_finder' : [13595], 'normal' : [13596], 'heroic' : [13597], 'mythic' : [13598]
    }
  }, {
    'id' : 2289, 'name' : "Blackwater Behemoth", 'raid_ids' : {
      'raid_finder' : [13591], 'normal' : [13592], 'heroic' : [13593], 'mythic' : [13594]
    }
  }, {
    'id' : 2304, 'name' : "Lady Ashvane", 'raid_ids' : {
      'raid_finder' : [13600], 'normal' : [13601], 'heroic' : [13602], 'mythic' : [13603]
    }
  }, {
    'id' : 2303, 'name' : "Orgozoa", 'raid_ids' : {
      'raid_finder' : [13604], 'normal' : [13605], 'heroic' : [13606], 'mythic' : [13607]
    }
  }, {
    'id' : 2311, 'name' : "The Queen's Court", 'raid_ids' : {
      'raid_finder' : [13608], 'normal' : [13609], 'heroic' : [13610], 'mythic' : [13611]
    }
  }, {
    'id' : 2293, 'name' : "Za'qul", 'raid_ids' : {
      'raid_finder' : [13612], 'normal' : [13613], 'heroic' : [13614], 'mythic' : [13615]
    }
  }, {
    'id' : 2299, 'name' : "Queen Azshara", 'raid_ids' : {
      'raid_finder' : [13616], 'normal' : [13617], 'heroic' : [13618], 'mythic' : [13619]
    }
  }]
}]
