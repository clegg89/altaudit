#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 clegg <clegg@baratheon>
#
# Distributed under terms of the MIT license.

"""
Change the name of an existing character and update the database
"""
import yaml
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from altaudit.models import Region, Realm, Character

## TODO:
#
# Add unit tests
# Remove empty realms in config

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    region = sys.argv[1]
    realmIn = sys.argv[2]
    characterIn = sys.argv[3]
    realmOut = sys.argv[4]
    characterOut = sys.argv[5]


    # If not changing realms, just update index
    if realmOut == realmIn:
        # Find the previous character in config
        index = config['characters'][region][realmIn].index(characterIn)
        config['characters'][region][realmOut][index] = characterOut
    else:
        # Different realms, delete old character and add new one
        config['characters'][region][realmIn].remove(characterIn)

        # Create the realm if it doesn't exist
        if realmOut not in config['characters'][region].keys():
            config['characters'][region][realmOut] = list()

        # Append to new list
        config['characters'][region][realmOut].append(characterOut)

    # Database stuff
    engine = create_engine(config['database'], echo=True)
    session = sessionmaker(engine)()

    try:
        # Find previous entry in db
        character_model = session.query(Character).\
                filter_by(name=characterIn).join(Realm).\
                filter_by(name=realmIn).join(Region).\
                filter_by(name=region).first()

        # Find realm we're moving to
        realm_out_model = session.query(Realm).\
                filter_by(name=realmOut).join(Region).\
                filter_by(name=region).first()

        # Error, not found
        if not character_model:
            print("Character Not Found")
            raise

        # New realm
        if not realm_out_model:
            realm_out_model = Realm(realmOut, character_model.realm.region)
            session.add(realm_out_model)

        # Update
        character_model.name = characterOut
        character_model.realm = realm_out_model

        # Update config
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
