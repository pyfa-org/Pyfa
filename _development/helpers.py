# noinspection PyPackageRequirements
import pytest

import os
import sys
import threading

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add root folder to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))
sys._called_from_test = True

# noinspection PyUnresolvedReferences,PyUnusedLocal
@pytest.fixture
def DBInMemory_test():
    def rollback():
        with sd_lock:
            saveddata_session.rollback()


    print("Creating database in memory")
    from os.path import realpath, join, dirname, abspath

    debug = False
    gamedataCache = True
    saveddataCache = True
    gamedata_version = ""
    gamedata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(str(__file__))), "..", "eve.db"))
    saveddata_connectionstring = 'sqlite:///:memory:'

    class ReadOnlyException(Exception):
        pass

    if callable(gamedata_connectionstring):
        gamedata_engine = create_engine("sqlite://", creator=gamedata_connectionstring, echo=debug)
    else:
        gamedata_engine = create_engine(gamedata_connectionstring, echo=debug)

    gamedata_meta = MetaData()
    gamedata_meta.bind = gamedata_engine
    gamedata_session = sessionmaker(bind=gamedata_engine, autoflush=False, expire_on_commit=False)()

    # This should be moved elsewhere, maybe as an actual query. Current, without try-except, it breaks when making a new
    # game db because we haven't reached gamedata_meta.create_all()
    try:
        gamedata_version = gamedata_session.execute(
            "SELECT `field_value` FROM `metadata` WHERE `field_name` LIKE 'client_build'"
        ).fetchone()[0]
    except Exception as e:
        print("Missing gamedata version.")
        gamedata_version = None

    if saveddata_connectionstring is not None:
        if callable(saveddata_connectionstring):
            saveddata_engine = create_engine(creator=saveddata_connectionstring, echo=debug)
        else:
            saveddata_engine = create_engine(saveddata_connectionstring, echo=debug)

        saveddata_meta = MetaData()
        saveddata_meta.bind = saveddata_engine
        saveddata_session = sessionmaker(bind=saveddata_engine, autoflush=False, expire_on_commit=False)()
    else:
        saveddata_meta = None

    # Lock controlling any changes introduced to session
    sd_lock = threading.Lock()

    # Import all the definitions for all our database stuff
    # noinspection PyPep8
    #from eos.db.gamedata import alphaClones, attribute, category, effect, group, icon, item, marketGroup, metaData, metaGroup, queries, traits, unit
    # noinspection PyPep8
    #from eos.db.saveddata import booster, cargo, character, crest, damagePattern, databaseRepair, drone, fighter, fit, implant, implantSet, loadDefaultDatabaseValues, miscData, module, override, price, queries, skill, targetResists, user

    # If using in memory saveddata, you'll want to reflect it so the data structure is good.
    if saveddata_connectionstring == "sqlite:///:memory:":
        saveddata_meta.create_all()

    # Output debug info to help us troubleshoot Travis
    print(saveddata_engine)
    print(gamedata_engine)

    helper = {
        #'config': eos.config,
        'gamedata_session'    : gamedata_session,
        'saveddata_session'    : saveddata_session,
    }
    return helper

# noinspection PyUnresolvedReferences,PyUnusedLocal
@pytest.fixture
def DBInMemory():
    print("Creating database in memory")

    import eos.config

    import eos
    import eos.db

    # Output debug info to help us troubleshoot Travis
    print((eos.db.saveddata_engine))
    print((eos.db.gamedata_engine))

    helper = {
        'config': eos.config,
        'db'    : eos.db,
        'gamedata_session' : eos.db.gamedata_session,
        'saveddata_session' : eos.db.saveddata_session,
    }
    return helper


@pytest.fixture
def Gamedata():
    print("Building Gamedata")
    from eos.gamedata import Item

    helper = {
        'Item': Item,
    }
    return helper


@pytest.fixture
def Saveddata():
    print("Building Saveddata")
    from eos.saveddata.ship import Ship
    from eos.saveddata.fit import Fit
    from eos.saveddata.character import Character
    from eos.saveddata.module import Module, State
    from eos.saveddata.citadel import Citadel
    from eos.saveddata.booster import Booster

    helper = {
        'Structure': Citadel,
        'Ship'     : Ship,
        'Fit'      : Fit,
        'Character': Character,
        'Module'   : Module,
        'State'    : State,
        'Booster'  : Booster,
    }
    return helper
