"""Character Processing"""
from .utility import Utility
from .sections import sections

def update_snapshots(character):
    year = Utility.year[self.region_name]
    week = Utility.week[self.region_name]
    if year not in self.snapshots:
        self.snapshots[year] = {}

    if week not in self.snapshots[year]:
        self.snapshots[year][week] = Snapshot()
        self.snapshots[year][week].world_quests = self.world_quests_total
        self.snapshots[year][week].dungeons = self.dungeons_total

def serialize_azerite(self):
    for slot in AZERITE_ITEM_SLOTS:
        for tier in range(AZERITE_TIERS):
            selected = getattr(self, '_{}_tier{}_selected'.format(slot, tier))
            selected = str(selected) if selected else None
            setattr(self, '{}_tier{}_selected'.format(slot, tier), selected)
            available = '|'.join([str(x) for x in getattr(self, '_{}_tier{}_available'.format(slot, tier))])
            setattr(self, '{}_tier{}_available'.format(slot, tier), available)

def serialize_gems(self):
    self.gem_ids = '|'.join([str(g.gem.id) for g in self.gems])
    self.gem_qualities = '|'.join([str(g.gem.quality) for g in self.gems])
    self.gem_names = '|'.join([str(g.gem.name) for g in self.gems])
    self.gem_icons = '|'.join([str(g.gem.icon) for g in self.gems])
    self.gem_stats = '|'.join([str(g.gem.stat) for g in self.gems])
    self.gem_slots = '|'.join([g.slot for g in self.gems])

def get_snapshots(self):
    weekly_snapshot = self.snapshots[Utility.year[self.region_name]][Utility.week[self.region_name]]
    self.world_quests_weekly = self.world_quests_total - weekly_snapshot.world_quests
    self.dungeons_weekly = self.dungeons_total - weekly_snapshot.dungeons

    # If something happened where snapshot total > our total, reset snapshot and set to 0
    if self.world_quests_weekly < 0:
        self.world_quests_weekly = 0
        weekly_snapshot.world_quests = self.world_quests_total
    if self.dungeons_weekly < 0:
        self.dungeons_weekly = 0
        weekly_snapshot.dungeons = self.dungeons_total

def process_blizzard(self, profile, db_session, api, force_refresh):
    """
    Processes the response from blizzard's API for this character

    Do not handle any exceptions that occur. If any part fails, we
    want to avoid updating the timestamp so that the character can
    get updated fully next time.

    @param profile The response from blizzard's api

    @param db_session The database session to use for queries

    @param api The api object used to make the request

    @param force_refresh If True will force the Character to update data
    """
    # Only update items that need the api if modified or forced
    if force_refresh or profile['last_login_timestamp'] != self.lastmodified:
        # Fetch rest of api
        for section in ['media', 'equipment']:
            profile[section] = api.get_data_resource(
                    '{}&locale={}'.format(profile['summary'][section], BLIZZARD_LOCALE),
                    self.region_name)

        # call each section, should loop like a pro
        sections = [f for _, f in Section.__dict__.items() if callable(f)]
        for section in sections:
            section(self, profile, db_session, api)

    # deep_fetch = force_refresh or profile['last_login_timestamp'] != self.lastmodified
    # conditional_api = api if deep_fetch else None

    # Section.basic(self, profile, db_session, conditional_api)
    # Section.items(self, profile)
    # Section.azerite(self, profile, db_session, conditional_api)
    # Section.audit(self, profile, db_session, conditional_api)
    # Section.professions(self, profile)
    # Section.reputations(self, profile)
    # Section.pve(self, profile)

    self._update_snapshots() # always update snapshots as we may go weeks without playing a character

def process_raiderio(self, response):
    """
    Processes the response from raider.io API for this character

    @param response The response from raider.io's API
    """
    if not response.ok:
        self.raiderio_score = 0
        self.mplus_weekly_highest = 0
        self.mplus_season_highest = 0
    else:
        Section.raiderio(self, response.json())

def serialize(self):
    self._serialize_azerite()
    self._serialize_gems()
    self._get_snapshots()
    return [getattr(self, field) for field in HEADERS]
