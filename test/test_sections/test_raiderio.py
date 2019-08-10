"""Unit Tests for RaiderIO Data"""
import pytest

from altaudit.models import Character

import altaudit.sections as Section

def test_raiderio_score():
    jack = Character('jack')
    response = {
            'mythic_plus_scores_by_season' : [
                { 'scores' : { 'all' : 400.0 } }
                ],
            'mythic_plus_highest_level_runs' : [],
            'mythic_plus_weekly_highest_level_runs' : []
            }

    Section.raiderio(jack, response)

    assert jack.raiderio_score == 400.0
    assert jack.mplus_weekly_highest == 0
    assert jack.mplus_season_highest == 0

def test_raiderio_weekly_and_season_highest():
    jack = Character('jack')
    response = {
            'mythic_plus_scores_by_season' : [
                { 'scores' : { 'all' : 0 } }
                ],
            'mythic_plus_highest_level_runs' : [
                {'mythic_level' : 12}
                ],
            'mythic_plus_weekly_highest_level_runs' : [
                {'mythic_level' : 7}
                ]
            }

    Section.raiderio(jack, response)

    assert jack.raiderio_score == 0.0
    assert jack.mplus_weekly_highest == 7
    assert jack.mplus_season_highest == 12
