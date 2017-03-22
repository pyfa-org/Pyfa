# noinspection PyPackageRequirements
import pytest

# noinspection PyUnresolvedReferences
from helpers import DBInMemory as DB
# noinspection PyUnresolvedReferences
from helpers import Gamedata
# noinspection PyUnresolvedReferences
from helpers import Saveddata


# noinspection PyShadowingNames
@pytest.fixture
def Rifter(DB, Gamedata, Saveddata):
    item = DB['db'].gamedata_session.query(Gamedata['Item']).filter(Gamedata['Item'].name == "Rifter").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "My Rifter Fit")

    return fit


# noinspection PyShadowingNames
def test_rifter_cpu_output(DB, Saveddata, Rifter):
    char5 = Saveddata['Character'].getAll5()
    char0 = Saveddata['Character'].getAll0()

    Rifter.character = char0
    mod = Saveddata['Module'](DB['db'].getItem("Co-Processor II"))
    mod.state = Saveddata['State'].OFFLINE
    Rifter.modules.append(mod)

    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 130

    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 130

    mod.state = Saveddata['State'].ONLINE
    Rifter.clear()
    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 143

    Rifter.character = char5
    Rifter.clear()
    Rifter.calculateModifiedAttributes()
    assert Rifter.ship.getModifiedItemAttr("cpuOutput") == 178.75

    # No reason to save it, but as an example how
    # DB['db'].save(Rifter)  # tada, it's now in database and can be accessed in pyfa
