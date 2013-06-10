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
        self.mwd = Module(db.getItem("1MN MicroWarpdrive II"))
        self.mwd.state = State.ACTIVE
        self.fit.modules.append(self.mwd)
        self.fit.calculateModifiedAttributes()

    def test_mass(self):
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.itemModifiedAttributes.original
        expected.increase("mass", self.mwd.getModifiedItemAttr("massAddition"))
        self.assertEquals(expected["mass"], self.fit.ship.getModifiedItemAttr("mass"))

    def test_speedboost(self):
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.itemModifiedAttributes.original
        maxVelBoost = self.mwd.getModifiedItemAttr("speedFactor") * self.mwd.getModifiedItemAttr("speedBoostFactor") / self.fit.ship.getModifiedItemAttr("mass")
        expected.boost("maxVelocity", maxVelBoost)
        self.assertEquals(expected["maxVelocity"], self.fit.ship.getModifiedItemAttr("maxVelocity"))

    def test_signature(self):
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.itemModifiedAttributes.original
        expected.boost("signatureRadius", self.mwd.getModifiedItemAttr("signatureRadiusBonus"))
        self.assertEquals(expected["signatureRadius"], self.fit.ship.getModifiedItemAttr("signatureRadius"))
