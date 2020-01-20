"""Update function to transfer/rename characters"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Region, Realm, Character

def _update_config(character_config, region, charIn, charOut):
    # If not changing realms, just update index
    if charOut['realm'] == charIn['realm']: # Find the previous character in config
        index = character_config[region][charIn['realm']].index(charIn['name'])
        character_config[region][charOut['realm']][index] = charOut['name']
    else:
        # Different realms, delete old character and add new one
        character_config[region][charIn['realm']].remove(charIn['name'])

        # If old realm is empty, delete it
        if not character_config[region][charIn['realm']]:
            del character_config[region][charIn['realm']]

        # Create the realm if it doesn't exist
        if charOut['realm'] not in character_config[region].keys():
            character_config[region][charOut['realm']] = list()

        # Append to new list
        character_config[region][charOut['realm']].append(charOut['name'])

def _update_db(database_config, region, charIn, charOut):
    engine = create_engine(database_config)
    session = sessionmaker(engine)()

    try:
        # Find previous entry in db
        character_model = session.query(Character).\
                filter_by(name=charIn['name']).join(Realm).\
                filter_by(name=charIn['realm']).join(Region).\
                filter_by(name=region).first()

        # Find realm we're moving to
        realm_out_model = session.query(Realm).\
                filter_by(name=charOut['name']).join(Region).\
                filter_by(name=region).first()

        # Error, not found
        if not character_model:
            print("Character Not Found")
            raise

        # New realm
        if not realm_out_model:
            realm_out_model = Realm(charOut['name'], character_model.realm.region)
            session.add(realm_out_model)

        # Update
        character_model.name = charOut['name']
        character_model.realm = realm_out_model

        # We do not need to delete empty realms as Audit class will take
        # care of that when it is run.

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def update(config, region, charIn, charOut):
    """
    Update a character's info (i.e. realm xfer and/or name change)

    @param config The config dict passed to Audit class
    @param region The region the character is in
    @param charIn Dictionary with keys:
        'realm' : Realm the character is in
        'name' : Name of the character
    @param charOut Dictionary with keys:
        'realm' : Realm the character is going to
        'name' : New name of the character
    """
    Utility._update_config(config['characters'], region, charIn, charOut)
    Utility._update_db(config['database'], region, charIn, charOut)
