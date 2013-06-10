from eos.tests import TestBase
from eos import db
from eos.types import Fit, Ship, Module
from eos.modifiedAttributeDict import ModifiedAttributeDict

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.fit.ship = Ship(db.getItem("Rifter"))
        self.testItem = db.getItem("Signal Amplifier II")
        self.testMod1 = Module(self.testItem)
        self.testMod2 = Module(self.testItem)
        self.fit.modules.append(self.testMod1)
        self.fit.modules.append(self.testMod2)
        self.fit.calculateModifiedAttributes()

    def test_scanResolution(self):
        self.buildTested = 171215
        targetAttrName = "scanResolution"
        penalize = True
        modBonus = self.testItem.getAttribute("scanResolutionBonus")
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, modBonus, stackingPenalties = penalize)
        expected.boost(targetAttrName, modBonus, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)

    def test_maxTargetRange(self):
        self.buildTested = 171215
        targetAttrName = "maxTargetRange"
        penalize = True
        modBonus = self.testItem.getAttribute("maxTargetRangeBonus")
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, modBonus, stackingPenalties = penalize)
        expected.boost(targetAttrName, modBonus, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)

    def test_maxLockedTargets(self):
        self.buildTested = 171215
        targetAttrName = "maxLockedTargets"
        modBonus = self.testItem.getAttribute("maxLockedTargetsBonus")
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.increase(targetAttrName, modBonus)
        expected.increase(targetAttrName, modBonus)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)
