from eos.tests import TestBase
from eos import db
from eos.types import Fit, Implant, Character, Ship

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.f = Fit()
        self.c = Character("testCR8")
        self.f.character = self.c
        self.f.ship = Ship(db.getItem("Rifter"))
        self.i = db.getItem("Hardwiring - Inherent Implants 'Squire' CR8")
        self.implant = Implant(self.i)
        self.f.implants.append(self.implant)
        self.f.calculateModifiedAttributes()

    def test_rechargeTimeBonus(self):
        original = self.f.ship.item.getAttribute("rechargeRate")
        self.assertAlmostEquals(original * 0.95, self.f.ship.getModifiedItemAttr("rechargeRate"))
