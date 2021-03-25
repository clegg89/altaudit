"""Unit Tests for covenant info"""
import pytest

from altaudit.models import Character

import altaudit.sections.covenant as Section

def test_covenant_get_covenant_from_profile():
    jack = Character('jack')
    response = { 'summary' : {
        'covenant_progress' : { 'chosen_covenant' : { 'name' : 'Night Fae' }}}}

    Section.covenant(jack, response, None)

    assert jack.covenant == 'Night Fae'
