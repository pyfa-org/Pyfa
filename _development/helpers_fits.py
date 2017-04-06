import pytest

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata


# noinspection PyShadowingNames
@pytest.fixture
def RifterFit(DB, Gamedata, Saveddata):
    print("Creating Rifter")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Rifter").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "My Rifter Fit")

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def KeepstarFit(DB, Gamedata, Saveddata):
    print("Creating Keepstar")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Keepstar").first()
    ship = Saveddata['Structure'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Keepstar Fit")

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def CurseFit(DB, Gamedata, Saveddata):
    print("Creating Curse - With Neuts")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Curse").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Curse - With Neuts")

    mod = Saveddata['Module'](DB['db'].getItem("Medium Energy Neutralizer II"))
    mod.state = Saveddata['State'].ONLINE

    # Add 5 neuts
    for _ in xrange(5):
        fit.modules.append(mod)

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def HeronFit(DB, Gamedata, Saveddata):
    print("Creating Heron - RemoteSebo")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Heron").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Heron - RemoteSebo")

    mod = Saveddata['Module'](DB['db'].getItem("Remote Sensor Booster II"))
    mod.state = Saveddata['State'].ONLINE

    # Add 5 neuts
    for _ in xrange(4):
        fit.modules.append(mod)

    return fit