from eos.tests import TestBase
from eos import db
from eos.types import Module, Fit, Ship

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.rifter = db.getItem("Rifter")
        self.fit.ship = Ship(self.rifter)
        self.relay = Module(db.getItem("Capacitor Power Relay I"))
        self.fit.modules.append(self.relay)
        self.fit.calculateModifiedAttributes()

    def test_CalcCrash(self):
        # Note, no calculation checking, just testing for a crash here.
        pass
