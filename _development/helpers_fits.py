import pytest

# noinspection PyPackageRequirements


# noinspection PyShadowingNames
@pytest.fixture
def RifterFit(DB, Gamedata, Saveddata):
    from eos.const import ImplantLocation
    print("Creating Rifter")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Rifter").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "My Rifter Fit")
    fit.implantLocation = ImplantLocation.FIT

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def KeepstarFit(DB, Gamedata, Saveddata):
    from eos.const import ImplantLocation
    print("Creating Keepstar")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Keepstar").first()
    ship = Saveddata['Structure'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Keepstar Fit")
    fit.implantLocation = ImplantLocation.FIT

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def CurseFit(DB, Gamedata, Saveddata):
    from eos.const import ImplantLocation
    print("Creating Curse - With Neuts")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Curse").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Curse - With Neuts")
    fit.implantLocation = ImplantLocation.FIT

    mod = Saveddata['Module'](DB['db'].getItem("Medium Energy Neutralizer II"))
    mod.state = Saveddata['State'].ONLINE

    # Add 5 neuts
    for _ in range(5):
        fit.modules.append(mod)

    return fit


# noinspection PyShadowingNames
@pytest.fixture
def HeronFit(DB, Gamedata, Saveddata):
    from eos.const import ImplantLocation
    print("Creating Heron - RemoteSebo")
    item = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Heron").first()
    ship = Saveddata['Ship'](item)
    # setup fit
    fit = Saveddata['Fit'](ship, "Heron - RemoteSebo")
    fit.implantLocation = ImplantLocation.FIT

    mod = Saveddata['Module'](DB['db'].getItem("Remote Sensor Booster II"))
    mod.state = Saveddata['State'].ONLINE

    # Add 5 neuts
    for _ in range(4):
        fit.modules.append(mod)

    return fit
