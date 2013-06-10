from eos.tests import TestBase
from eos import db
from eos.types import Module, Fit, Ship, State

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.i = db.getItem("Stasis Webifier I")
        self.f = Fit()
        self.f.ship = Ship(db.getItem("Rifter"))
        self.m = Module(self.i)
        self.m2 = Module(self.i)
        self.m.state = State.ACTIVE
        self.m2.state = State.ACTIVE
        self.f.projectedModules.append(self.m)
        self.f.projectedModules.append(self.m2)
        self.f.calculateModifiedAttributes()

    def test_speedSlow(self):
        original = self.f.ship.item.getAttribute("maxVelocity")
        multiplier = 0.5
        expected = original * (1 + (multiplier -1) * 0.86911998)  * multiplier
        self.assertAlmostEquals(expected, self.f.ship.getModifiedItemAttr("maxVelocity"), 3)
