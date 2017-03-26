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
