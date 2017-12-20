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
from _development.helpers_fits import RifterFit
from eos.graph.fitDps import FitDpsGraph

def test_fit_dps(DB, Saveddata, RifterFit):
    """
    Tests applied damage
    """

    # set pilot
    char0 = Saveddata['Character'].getAll0()
    RifterFit.character = char0

    # add a turret
    mod = Saveddata['Module'](DB['db'].getItem("280mm Howitzer Artillery II"))
    mod.state = Saveddata['State'].ACTIVE
    # there must be a better way to fetch this ammo directly, but I couldn't figure out the appropriate Gamedata voodoo
    # this, for example, did not work:
    # mod.charge = DB['gamedata_session'].query(Gamedata['Item']).filter(Gamedata['Item'].name == "EMP S").first()
    for charge in mod.getValidCharges():
        if charge.name == "EMP S":
            mod.charge = charge
            break
    RifterFit.modules.append(mod)
    mod.owner = RifterFit

    # update values
    RifterFit.clear()
    RifterFit.calculateModifiedAttributes()

    # calculate applied DPS
    graph = FitDpsGraph(RifterFit)
    data = graph.defaults.copy()
    data['emRes'] = 10.0
    data['distance'] = 7.0
    data['signatureRadius'] = 50.0
    data['tgtAngle'] = 90.0
    data['tgtSpeed'] = 100.0
    dps = graph.calcDps(data)

    assert abs(dps - 8.6) < 0.05
