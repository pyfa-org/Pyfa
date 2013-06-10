from eos.tests import TestBase
from eos import db
from eos.types import Fit, Ship

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.i = db.getItem("Warrior TP-300")
        self.f = Fit()
        self.f.ship = Ship(db.getItem("Rifter"))
        d = self.f.projectedDrones.appendItem(self.i, 2)
        d.amountActive = 2
        self.f.calculateModifiedAttributes()

    def test_speedSlow(self):
        original = self.f.ship.item.getAttribute("signatureRadius")
        multiplier = 1.04
        expected = original * (1 + (multiplier -1) * 0.86911998)  * multiplier
        self.assertAlmostEquals(expected, self.f.ship.getModifiedItemAttr("signatureRadius"), 3)
