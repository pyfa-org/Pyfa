import pytest

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata


# noinspection PyShadowingNames
@pytest.fixture
def StrongBluePillBooster (DB, Gamedata, Saveddata):
    print("Creating Strong Blue Pill Booster")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Strong Blue Pill Booster").first()
    return Saveddata['Booster'](item)
