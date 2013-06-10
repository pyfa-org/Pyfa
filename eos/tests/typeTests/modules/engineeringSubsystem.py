from eos.tests import TestBase
from eos import db
from eos.types import Module, Fit, Ship

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.tengu = db.getItem("Tengu")
        self.fit.ship = Ship(self.tengu)
        self.sub = Module(db.getItem("Tengu Engineering - Augmented Capacitor Reservoir"))
        self.fit.modules.append(self.sub)
        self.fit.calculateModifiedAttributes()

    def test_hardening(self):
        self.assertGreater(self.fit.ship.getModifiedItemAttr("powerOutput"), 0)
