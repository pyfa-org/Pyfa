# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import math
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.realpath(os.path.join(script_dir, '..', '..', '..'))
print script_dir
sys.path.append(script_dir)

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
from _development.helpers_fits import RifterFit, KeepstarFit
from eos.graph.fitDps import FitDpsGraph

def test_turret_dps(DB, Saveddata, RifterFit):
    """
    Tests applied turret damage
    """

    # set pilot
    char0 = Saveddata['Character'].getAll0()
    RifterFit.character = char0

    # configure DPS analysis to include as many factors as possible
    # (damage type reistance, distance past turret optimal, sig/speed/angle to incur turret tracking penalty)
    graph = FitDpsGraph(RifterFit)
    data = graph.defaults.copy()
    data['emRes'] = 10.0
    data['distance'] = 7.0
    data['signatureRadius'] = 100.0
    data['tgtAngle'] = 90.0
    data['tgtSpeed'] = 100.0

    # add a turret
    mod = Saveddata['Module'](DB['db'].getItem("280mm Howitzer Artillery II"))
    mod.owner = RifterFit
    mod.state = Saveddata['State'].ACTIVE
    # there must be a better way to fetch this ammo directly, but I couldn't figure out the appropriate Gamedata voodoo;
    # this, for example, did not work:
    # mod.charge = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "EMP S").first()
    for charge in mod.getValidCharges():
        if charge.name == "EMP S":
            mod.charge = charge
            break
    RifterFit.modules.append(mod)

    # calculate applied DPS
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()
    dps = graph.calcDps(data)
    assert abs(dps - 8.8) < 0.05

def test_missile_dps(DB, Saveddata, RifterFit):
    """
    Tests applied missile damage
    """

    # set pilot
    char0 = Saveddata['Character'].getAll0()
    RifterFit.character = char0

    # configure DPS analysis to include as many factors as possible
    # (damage type reistance, sig/speed to incur missile application penalty)
    graph = FitDpsGraph(RifterFit)
    data = graph.defaults.copy()
    data['emRes'] = 10.0
    data['distance'] = 7.0
    data['signatureRadius'] = 100.0
    data['tgtSpeed'] = 100.0

    # add a launcher
    mod = Saveddata['Module'](DB['db'].getItem("Heavy Missile Launcher II"))
    mod.owner = RifterFit
    mod.state = Saveddata['State'].ACTIVE
    # there must be a better way to fetch this ammo directly, but I couldn't figure out the appropriate Gamedata voodoo;
    # this, for example, did not work:
    # mod.charge = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "Mjolnir Heavy Missile").first()
    for charge in mod.getValidCharges():
        if charge.name == "Mjolnir Heavy Missile":
            mod.charge = charge
            break
    RifterFit.modules.append(mod)

    # calculate applied DPS
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()
    dps = graph.calcDps(data)
    assert abs(dps - 7.3) < 0.05

def test_drone_dps(DB, Saveddata, RifterFit):
    """
    Tests applied drone damage
    """

    # set pilot
    char0 = Saveddata['Character'].getAll0()
    RifterFit.character = char0

    # configure DPS analysis to include as many factors as possible
    # (damage type reistance)
    graph = FitDpsGraph(RifterFit)
    data = graph.defaults.copy()
    data['emRes'] = 10.0

    # add a drone
    drone = Saveddata['Drone'](DB['db'].getItem("Acolyte II"))
    drone.amount = 1
    drone.amountActive = 1
    RifterFit.drones.append(drone)

    # calculate applied DPS
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()
    dps = graph.calcDps(data)
    assert abs(dps - 7.6) < 0.05

def test_fighter_dps(DB, Saveddata, KeepstarFit):
    """
    Tests applied fighter damage
    """

    # set pilot
    char0 = Saveddata['Character'].getAll0()
    KeepstarFit.character = char0

    # configure DPS analysis to include as many factors as possible
    # (damage type reistance)
    graph = FitDpsGraph(KeepstarFit)
    data = graph.defaults.copy()
    data['emRes'] = 10.0

    # add a fighter
    KeepstarFit.modules.clear()
    fighter = Saveddata['Fighter'](DB['db'].getItem("Equite II"))
    fighter.amountActive = 1
    KeepstarFit.fighters.append(fighter)

    # calculate applied DPS
    KeepstarFit.clear()
    KeepstarFit.calculateModifiedAttributes()
    dps = graph.calcDps(data)
    assert abs(dps - 10.8) < 0.05
