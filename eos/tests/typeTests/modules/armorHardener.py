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
        self.hardener = Module(db.getItem("Armor EM Hardener II"))
        self.hardener.state = State.ACTIVE
        self.fit.modules.append(self.hardener)
        self.fit.calculateModifiedAttributes()

    def test_hardening(self):
        expected = ModifiedAttributeDict()
        expected.original = self.rifter.attributes
        expected.boost("armorEmDamageResonance", self.hardener.getModifiedItemAttr("emDamageResistanceBonus"))
        self.assertEquals(expected["armorEmDamageResonance"], self.fit.ship.getModifiedItemAttr("armorEmDamageResonance"))
