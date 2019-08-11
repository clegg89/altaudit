"""Pull RaiderIO Data from API"""

def raiderio(character, response):
    character.raiderio_score = response['mythic_plus_scores_by_season'][0]['scores']['all']
    mplus = {
            'weekly_highest' : response['mythic_plus_weekly_highest_level_runs'],
            'season_highest' : response['mythic_plus_highest_level_runs']
            }

    print(character.name)
    for metric,data in mplus.items():
        setattr(character, 'mplus_{}'.format(metric), data[0]['mythic_level'] if len(data) > 0 else 0)
