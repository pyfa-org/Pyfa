# noinspection PyPackageRequirements
import pytest


# noinspection PyUnresolvedReferences,PyUnusedLocal
@pytest.fixture
def DBInMemory():
    import eos.config
    from os.path import realpath, join, dirname, abspath

    debug = False
    gamedataCache = True
    saveddataCache = True
    gamedata_version = ""
    eos.config.gamedata_connectionstring = 'sqlite:///' + realpath(join(dirname(abspath(unicode(__file__))), "..", "..", "eve.db"))
    # saveddata_connectionstring = 'sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "saveddata", "saveddata.db")), sys.getfilesystemencoding())
    eos.config.saveddata_connectionstring = 'sqlite:///:memory:'

    import eos
    import eos.db

    # Output debug info to help us troubleshoot Travis
    print(eos.db.saveddata_engine)
    print(eos.db.gamedata_engine)

    helper = {
        'config': eos.config,
        'db'    : eos.db,
    }
    return helper


@pytest.fixture
def Gamedata():
    from eos.gamedata import Item

    helper = {
        'Item': Item,
    }
    return helper


@pytest.fixture
def Saveddata():
    from eos.saveddata.ship import Ship
    from eos.saveddata.fit import Fit
    from eos.saveddata.character import Character
    from eos.saveddata.module import Module, State

    helper = {
        'Ship'     : Ship,
        'Fit'      : Fit,
        'Character': Character,
        'Module'   : Module,
        'State'    : State,
    }
    return helper
