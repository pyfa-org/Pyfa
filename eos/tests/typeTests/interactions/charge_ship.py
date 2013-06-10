from eos import db
from eos.tests import TestBase
from eos.types import Fit, Character, Ship, Module, State

class Test(TestBase):
    def test_scanResolution_ship(self):
        iIngame = 1.0
        fIngame = 1.6
        fit = Fit()
        char = Character("test")
        fit.character = char
        fit.ship = Ship(db.getItem("Rifter"))
        iEos = fit.ship.getModifiedItemAttr("scanResolution")
        mod = Module(db.getItem("Sensor Booster II"))
        mod.charge = db.getItem("Scan Resolution")
        mod.state = State.ACTIVE
        fit.modules.append(mod)
        fit.calculateModifiedAttributes()
        fEos = fit.ship.getModifiedItemAttr("scanResolution")
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_scanResolution_ship_2(self):
        iIngame = 1.0
        fIngame = 1.6
        fit = Fit()
        char = Character("test")
        fit.character = char
        fit.ship = Ship(db.getItem("Rifter"))
        fit.calculateModifiedAttributes()
        iEos = fit.ship.getModifiedItemAttr("scanResolution")
        mod = Module(db.getItem("Sensor Booster II"))
        mod.charge = db.getItem("Scan Resolution")
        mod.state = State.ACTIVE
        fit.modules.append(mod)
        fit.clear()
        fit.calculateModifiedAttributes()
        fEos = fit.ship.getModifiedItemAttr("scanResolution")
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
