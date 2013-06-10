from eos.tests import TestBase
from eos import db
from eos.types import Module, Fit, Ship, State
from eos.modifiedAttributeDict import ModifiedAttributeDict

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.rifter = db.getItem("Rifter")
        self.fit.ship = Ship(self.rifter)
        self.afterburner = Module(db.getItem("1MN Afterburner II"))
        self.afterburner.state = State.ACTIVE
        self.fit.modules.append(self.afterburner)
        self.fit.calculateModifiedAttributes()

    def test_mass(self):
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.itemModifiedAttributes.original
        expected.increase("mass", self.afterburner.getModifiedItemAttr("massAddition"))
        self.assertEquals(expected["mass"], self.fit.ship.getModifiedItemAttr("mass"))

    def test_speedboost(self):
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.itemModifiedAttributes.original
        maxVelBoost = self.afterburner.getModifiedItemAttr("speedFactor") * self.afterburner.getModifiedItemAttr("speedBoostFactor") / self.fit.ship.getModifiedItemAttr("mass")
        expected.boost("maxVelocity", maxVelBoost)
        self.assertEquals(expected["maxVelocity"], self.fit.ship.getModifiedItemAttr("maxVelocity"))
