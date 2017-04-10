# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
from time import time
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))

#
# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
# noinspection PyPackageRequirements
from _development.helpers_fits import RifterFit, KeepstarFit, HeronFit, CurseFit
from service.fit import Fit
#
# # Fake import wx
# # todo: fix this
# # from types import ModuleType
# # wx = ModuleType("fake_module")
# # sys.modules[wx.__name__] = wx
#
# def test_getAllFits(DB, RifterFit, KeepstarFit):
#     assert len(Fit.getAllFits()) == 0
#     DB['db'].save(RifterFit)
#     assert len(Fit.getAllFits()) == 1
#     DB['db'].save(KeepstarFit)
#     assert len(Fit.getAllFits()) == 2
#
#     # Cleanup after ourselves
#     DB['db'].remove(RifterFit)
#     DB['db'].remove(KeepstarFit)
#
#
# def test_getFitsWithShip_RifterFit(DB, RifterFit):
#     DB['db'].save(RifterFit)
#
#     assert Fit.getFitsWithShip(587)[0][1] == 'My Rifter Fit'
#
#     DB['db'].remove(RifterFit)


def test_RifterSingleNew(DB, RifterFit, KeepstarFit, HeronFit, CurseFit):
    DB['db'].save(RifterFit)
    DB['db'].save(KeepstarFit)
    DB['db'].save(HeronFit)
    DB['db'].save(CurseFit)
    sFit = Fit.getInstance()
    sFit.serviceFittingOptions = {
        "useGlobalCharacter"    : False,
        "useGlobalDamagePattern": False,
        "useGlobalForceReload"  : False,
        "colorFitBySlot"        : False,
        "rackSlots"             : True,
        "rackLabels"            : True,
        "compactSkills"         : True,
        "showTooltip"           : True,
        "showMarketShortcuts"   : False,
        "enableGaugeAnimation"  : True,
        "exportCharges"         : True,
        "openFitInNew"          : False,
        "priceSystem"           : "Jita",
        "showShipBrowserTooltip": True,
    }

    cached_fits = []
    fit = DB["db"].getFit(1)
    cached_fits.append(fit)
    fit = None

    time_start = time()

    for _ in xrange(1000000):

        fit = next((x for x in cached_fits if x.ID == 1), None)

        fit = None

    print("1000000 of the Rifter fit (new): " + str(time()-time_start))

    # fit = DB["db"].getFit(1)

    # Cleanup after ourselves
    DB['db'].remove(RifterFit)
    DB['db'].remove(KeepstarFit)
    DB['db'].remove(HeronFit)
    DB['db'].remove(CurseFit)

def test_RifterSingleOld(DB, RifterFit, KeepstarFit, HeronFit, CurseFit):
    DB['db'].save(RifterFit)
    DB['db'].save(KeepstarFit)
    DB['db'].save(HeronFit)
    DB['db'].save(CurseFit)
    sFit = Fit.getInstance()
    sFit.serviceFittingOptions = {
        "useGlobalCharacter"    : False,
        "useGlobalDamagePattern": False,
        "useGlobalForceReload"  : False,
        "colorFitBySlot"        : False,
        "rackSlots"             : True,
        "rackLabels"            : True,
        "compactSkills"         : True,
        "showTooltip"           : True,
        "showMarketShortcuts"   : False,
        "enableGaugeAnimation"  : True,
        "exportCharges"         : True,
        "openFitInNew"          : False,
        "priceSystem"           : "Jita",
        "showShipBrowserTooltip": True,
    }

    cached_fits = []
    fit = DB["db"].getFit(1)
    cached_fits.append(fit)
    fit = None

    time_start = time()

    for _ in xrange(1000000):

        fit = DB["db"].getFit(1)

        fit = None

    print("1000000 of the Rifter fit (old): " + str(time()-time_start))

    # Cleanup after ourselves
    DB['db'].remove(RifterFit)
    DB['db'].remove(KeepstarFit)
    DB['db'].remove(HeronFit)
    DB['db'].remove(CurseFit)

def test_FourNew(DB, RifterFit, KeepstarFit, HeronFit, CurseFit):
    DB['db'].save(RifterFit)
    DB['db'].save(KeepstarFit)
    DB['db'].save(HeronFit)
    DB['db'].save(CurseFit)
    sFit = Fit.getInstance()
    sFit.serviceFittingOptions = {
        "useGlobalCharacter"    : False,
        "useGlobalDamagePattern": False,
        "useGlobalForceReload"  : False,
        "colorFitBySlot"        : False,
        "rackSlots"             : True,
        "rackLabels"            : True,
        "compactSkills"         : True,
        "showTooltip"           : True,
        "showMarketShortcuts"   : False,
        "enableGaugeAnimation"  : True,
        "exportCharges"         : True,
        "openFitInNew"          : False,
        "priceSystem"           : "Jita",
        "showShipBrowserTooltip": True,
    }

    cached_fits = []
    fit = DB["db"].getFit(1)
    cached_fits.append(fit)
    fit = None

    time_start = time()

    for _ in xrange(250000):

        fit = next((x for x in cached_fits if x.ID == 1), None)
        fit = None
        fit = next((x for x in cached_fits if x.ID == 2), None)
        fit = None
        fit = next((x for x in cached_fits if x.ID == 3), None)
        fit = None
        fit = next((x for x in cached_fits if x.ID == 4), None)
        fit = None


    print("1000000 of the four fits (new): " + str(time()-time_start))

    # fit = DB["db"].getFit(1)

    # Cleanup after ourselves
    DB['db'].remove(RifterFit)
    DB['db'].remove(KeepstarFit)
    DB['db'].remove(HeronFit)
    DB['db'].remove(CurseFit)

def test_FourOld(DB, RifterFit, KeepstarFit, HeronFit, CurseFit):
    DB['db'].save(RifterFit)
    DB['db'].save(KeepstarFit)
    DB['db'].save(HeronFit)
    DB['db'].save(CurseFit)
    sFit = Fit.getInstance()
    sFit.serviceFittingOptions = {
        "useGlobalCharacter"    : False,
        "useGlobalDamagePattern": False,
        "useGlobalForceReload"  : False,
        "colorFitBySlot"        : False,
        "rackSlots"             : True,
        "rackLabels"            : True,
        "compactSkills"         : True,
        "showTooltip"           : True,
        "showMarketShortcuts"   : False,
        "enableGaugeAnimation"  : True,
        "exportCharges"         : True,
        "openFitInNew"          : False,
        "priceSystem"           : "Jita",
        "showShipBrowserTooltip": True,
    }

    cached_fits = []
    fit = DB["db"].getFit(1)
    cached_fits.append(fit)
    fit = None

    time_start = time()

    for _ in xrange(250000):

        fit = DB["db"].getFit(1)
        fit = None
        fit = DB["db"].getFit(2)
        fit = None
        fit = DB["db"].getFit(3)
        fit = None
        fit = DB["db"].getFit(4)
        fit = None

    print("1000000 of the four fits (old): " + str(time()-time_start))

    # Cleanup after ourselves
    DB['db'].remove(RifterFit)
    DB['db'].remove(KeepstarFit)
    DB['db'].remove(HeronFit)
    DB['db'].remove(CurseFit)

