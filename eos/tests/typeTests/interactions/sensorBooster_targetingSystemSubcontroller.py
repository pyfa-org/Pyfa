from eos.tests import TestBase
from eos import db
from eos.types import Fit, Ship, Module, State
from eos.modifiedAttributeDict import ModifiedAttributeDict

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.fit.ship = Ship(db.getItem("Rifter"))
        self.sensBoostItem = db.getItem("Sensor Booster II")
        self.t1RigItem = db.getItem("Small Targeting System Subcontroller I")
        self.t2RigItem = db.getItem("Small Targeting System Subcontroller II")
        self.sensBoostMod = Module(self.sensBoostItem)
        self.t1RigMod = Module(self.t1RigItem)
        self.t2RigMod = Module(self.t2RigItem)
        self.sensBoostMod.state = State.ACTIVE

    def test_scanResolutionT1(self):
        self.buildTested = 171215
        self.fit.modules.append(self.sensBoostMod)
        self.fit.modules.append(self.t1RigMod)
        self.fit.calculateModifiedAttributes()
        targetAttrName = "scanResolution"
        penalize = False
        sensBoostBoost = self.sensBoostItem.getAttribute("scanResolutionBonus")
        t1RigMultiplier = self.t1RigItem.getAttribute("scanResolutionMultiplier")
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, sensBoostBoost, stackingPenalties = penalize)
        expected.multiply(targetAttrName, t1RigMultiplier, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)

    def test_scanResolutionT2(self):
        self.buildTested = 171215
        self.fit.modules.append(self.sensBoostMod)
        self.fit.modules.append(self.t2RigMod)
        self.fit.calculateModifiedAttributes()
        targetAttrName = "scanResolution"
        penalize = False
        sensBoostBoost = self.sensBoostItem.getAttribute("scanResolutionBonus")
        t2RigMultiplier = self.t2RigItem.getAttribute("scanResolutionMultiplier")
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, sensBoostBoost, stackingPenalties = penalize)
        expected.multiply(targetAttrName, t2RigMultiplier, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)
