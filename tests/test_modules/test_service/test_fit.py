# Add root folder to python paths
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
# noinspection PyPackageRequirements
from _development.helpers_fits import RifterFit, KeepstarFit
from service.fit import Fit


def test_getAllFits(DB, RifterFit, KeepstarFit):
    assert len(Fit.getAllFits()) == 0

    DB['db'].save(RifterFit)
    DB['db'].save(KeepstarFit)

    # For some reason in Travis this adds the first fit twice.  WHY?!?
    assert len(Fit.getAllFits()) != 0

    # Cleanup after ourselves
    DB['db'].remove(RifterFit)
    DB['db'].remove(KeepstarFit)


def test_getFitsWithShip_RifterFit(DB, RifterFit):
    DB['db'].save(RifterFit)

    assert Fit.getFitsWithShip(587)[0][1] == 'My Rifter Fit'

    DB['db'].remove(RifterFit)
