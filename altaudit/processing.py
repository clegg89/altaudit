"""Character Processing"""
import logging
import datetime

from wowapi import WowApiException

from .utility import Utility, WEEKLY_RESETS
from .sections import sections, raiderio
from .models import Snapshot, AZERITE_ITEM_SLOTS, AZERITE_TIERS, HEADERS
from .blizzard import BLIZZARD_LOCALE

PROFILE_API_SECTIONS = ['media', 'equipment', 'reputations', {'achievements' : 'statistics'}, {'quests' : 'completed'}]

def _serialize_azerite(character):
    for slot in AZERITE_ITEM_SLOTS:
        for tier in range(AZERITE_TIERS):
            selected = getattr(character, '_{}_tier{}_selected'.format(slot, tier))
            selected = str(selected) if selected else None
            setattr(character, '{}_tier{}_selected'.format(slot, tier), selected)
            available = getattr(character, '_{}_tier{}_available'.format(slot, tier))
            available = '|'.join([str(x) for x in available]) if available else None
            setattr(character, '{}_tier{}_available'.format(slot, tier), available)

def _serialize_gems(character):
    character.gem_ids = '|'.join([str(g.gem.id) for g in character.gems])
    character.gem_qualities = '|'.join([str(g.gem.quality) for g in character.gems])
    character.gem_names = '|'.join([str(g.gem.name) for g in character.gems])
    character.gem_icons = '|'.join([str(g.gem.icon) for g in character.gems])
    character.gem_stats = '|'.join([str(g.gem.stat) for g in character.gems])
    character.gem_slots = '|'.join([g.slot for g in character.gems])

def _get_snapshots(character):
    try:
        weekly_snapshot = character.snapshots[Utility.year[character.region_name]][Utility.week[character.region_name]]
        character.world_quests_weekly = character.world_quests_total - weekly_snapshot.world_quests
        character.dungeons_weekly = character.dungeons_total - weekly_snapshot.dungeons

        # If something happened where snapshot total > our total, reset snapshot and set to 0
        if character.world_quests_weekly < 0:
            character.world_quests_weekly = 0
            weekly_snapshot.world_quests = character.world_quests_total
        if character.dungeons_weekly < 0:
            character.dungeons_weekly = 0
            weekly_snapshot.dungeons = character.dungeons_total

    except KeyError:
        pass
    except:
        logger = logging.getLogger('altaudit')
        logger.exception("Unknown error in snapshot")

def _fill_missing_snapshots(character):
    """
    The question is, should we do this EVERY time through the loop?
    Only occasionally? Manually? 99% of the time this will do absolutely
    nothing. But its also hard to tell when snapshots ARE missing from
    looking at the output (can you remember how many dungeons/wqs you ran
    on the 20th week of 2017? what was your highest key that week?)

    Good compromise: Run whenever a new snapshot is created (1/week)
    """
    reset_day = WEEKLY_RESETS[character.region_name]['day']
    reset_hour = WEEKLY_RESETS[character.region_name]['hour']
    start_year = min(character.snapshots.keys())
    start_year_week = min(character.snapshots[start_year].keys())
    stop_year = max(character.snapshots.keys())
    stop_year_week = max(character.snapshots[stop_year].keys())
    start_date = datetime.datetime.combine(datetime.date.fromisocalendar(start_year, start_year_week, reset_day),
            datetime.time(reset_hour))
    stop_date = datetime.datetime.combine(datetime.date.fromisocalendar(stop_year, stop_year_week, reset_day),
            datetime.time(reset_hour))

    world_quests = character.snapshots[start_year][start_year_week].world_quests
    dungeons = character.snapshots[start_year][start_year_week].dungeons

    test_date = start_date
    while test_date < stop_date:
        year = test_date.isocalendar()[0]
        week = test_date.isocalendar()[1]
        if year not in character.snapshots:
            character.snapshots[year] = {}

        if week not in character.snapshots[year]:
            character.snapshots[year][week] = Snapshot()
            character.snapshots[year][week].world_quests = world_quests
            character.snapshots[year][week].dungeons = dungeons

        world_quests = character.snapshots[year][week].world_quests
        dungeons = character.snapshots[year][week].dungeons

        test_date += datetime.timedelta(7)

def _get_historical_data(character):
    world_quests = []
    dungeons = []
    mplus = []
    all_snapshots = [character.snapshots[year][week]
            for year in sorted(character.snapshots.keys())
            for week in sorted(character.snapshots[year].keys())]

    for index,snapshot in enumerate(all_snapshots[1:]):
        world_quests.insert(0, snapshot.world_quests - all_snapshots[index].world_quests)
        dungeons.insert(0, snapshot.dungeons - all_snapshots[index].dungeons)
        mplus.insert(0, all_snapshots[index].highest_mplus) # will skip the last one

    character.historic_world_quests_done = '|'.join([str(wq) for  wq in world_quests])
    character.historic_dungeons_done = '|'.join([str(d) for d in dungeons])
    character.historic_mplus_done = '|'.join([str(mp) if mp else '0' for mp in mplus])

def _get_subsections(region, profile, api, sub_section, parent='summary', prefix=''):
    if type(sub_section) is str:
        if profile[parent] and sub_section in profile[parent]:
            try:
                profile[prefix + sub_section] = api.get_data_resource(
                        '{}&locale={}'.format(profile[parent][sub_section]['href'], BLIZZARD_LOCALE), region)
            except WowApiException:
                profile[prefix + sub_section] = None
        else:
            profile[prefix + sub_section] = None
    elif type(sub_section) is list:
        for section in sub_section:
            _get_subsections(region, profile, api, section, parent, prefix)
    elif type(sub_section) is dict:
        for k,v in sub_section.items():
            _get_subsections(region, profile, api, k, parent, prefix)
            _get_subsections(region, profile, api, v, k, prefix + k + '_')

def update_snapshots(character):
    logger = logging.getLogger('altaudit')

    year = Utility.year[character.region_name]
    week = Utility.week[character.region_name]
    prev_week_year = Utility.prev_week_year[character.region_name]
    prev_week_week = Utility.prev_week_week[character.region_name]
    if year not in character.snapshots:
        character.snapshots[year] = {}

    if week not in character.snapshots[year] and \
            character.world_quests_total is not None and character.dungeons_total is not None:
        logger.debug("Week %i of %i not found, setting %i, %i, %i", year, week, character.world_quests_total, character.dungeons_total, character.mplus_weekly_highest)
        character.snapshots[year][week] = Snapshot()
        character.snapshots[year][week].world_quests = character.world_quests_total
        character.snapshots[year][week].dungeons = character.dungeons_total
        try:
            character.snapshots[prev_week_year][prev_week_week].highest_mplus = character.mplus_weekly_highest
        except KeyError:
            pass

        _fill_missing_snapshots(character)

def process_blizzard(character, profile, db_session, api, force_refresh):
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
    if force_refresh or profile['summary']['last_login_timestamp'] != character.lastmodified:
        # Fetch rest of api
        _get_subsections(character.region_name, profile, api, PROFILE_API_SECTIONS)

        # call each section, should loop like a pro
        for section in sections:
            section(character, profile, db_session, api)

def process_raiderio(character, response):
    """
    Processes the response from raider.io API for this character

    @param response The response from raider.io's API
    """
    if not response.ok:
        character.raiderio_score = 0
        character.mplus_weekly_highest = 0
        character.mplus_season_highest = 0
    else:
        raiderio(character, response.json())

def serialize(character):
    _serialize_azerite(character)
    _serialize_gems(character)
    _get_snapshots(character)
    _get_historical_data(character)
    return [getattr(character, field) for field in HEADERS]
