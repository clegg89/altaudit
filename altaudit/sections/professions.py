"""Pull Profession Data from API Response"""

from ..models import PROFESSIONS, PROFESSION_EXPACS, PROFESSION_FIELD_COLUMNS

"Profession Fields"
PROFESSION_FIELDS = [f[0] for f in PROFESSION_FIELD_COLUMNS]

def professions(character, response):
    profession_response = response['professions']

    for prof in PROFESSIONS:
        for field in PROFESSION_FIELDS:
            setattr(character, '{}_{}'.format(prof, field), None)

    professions = {}
    for prof_type in ['primary', 'secondary']:
        professions[prof_type] = {}
        for prof in profession_response[prof_type]:
            prof_name = prof['name'].split(' ')
            name = prof_name[-1]
            expac = PROFESSION_EXPACS[' '.join(prof_name[:-1])]
            rank = prof['rank']
            max_rank = prof['max'] if not expac == 'battle_for_azeroth' else 175

            if name not in professions[prof_type]:
                professions[prof_type][name] = {
                        'name' : name,
                        'icon' : prof['icon'] if 'icon' in prof else None}

            if 'icon' in prof and not professions[prof_type][name]['icon']:
                professions[prof_type][name]['icon'] = prof['icon']

            professions[prof_type][name]['{}_level'.format(expac)] = rank
            professions[prof_type][name]['{}_max'.format(expac)] = max_rank

    for idx,primary in enumerate(professions['primary'].values()):
        for field,value in primary.items():
            setattr(character, 'primary{}_{}'.format(idx+1,field), value)

    for secondary in ('Cooking', 'Fishing'):
        for field,value in professions['secondary'][secondary].items():
            setattr(character, '{}_{}'.format(secondary.lower(), field), value)

    for field in ('level', 'max'):
        professions['secondary']['Archaeology'][field] = professions['secondary']['Archaeology'].pop('classic_{}'.format(field))

    for field,value in professions['secondary']['Archaeology'].items():
        setattr(character, 'archaeology_{}'.format(field), value)
