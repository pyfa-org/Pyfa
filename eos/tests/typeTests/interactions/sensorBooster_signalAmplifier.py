from eos.tests import TestBase
from eos import db
from eos.types import Fit, Ship, Module, State
from eos.modifiedAttributeDict import ModifiedAttributeDict

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.fit = Fit()
        self.fit.ship = Ship(db.getItem("Rifter"))
        self.testItem1 = db.getItem("Sensor Booster II")
        self.testItem2 = db.getItem("Signal Amplifier II")
        self.testMod1 = Module(self.testItem1)
        self.testMod2 = Module(self.testItem2)
        self.testMod1.state = State.ACTIVE
        self.fit.modules.append(self.testMod1)
        self.fit.modules.append(self.testMod2)
        self.fit.calculateModifiedAttributes()

    def test_scanResolution(self):
        self.buildTested = 171215
        bonusAttrName = "scanResolutionBonus"
        targetAttrName = "scanResolution"
        penalize = True
        mod1Bonus = self.testItem1.getAttribute(bonusAttrName)
        mod2Bonus = self.testItem2.getAttribute(bonusAttrName)
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, mod1Bonus, stackingPenalties = penalize)
        expected.boost(targetAttrName, mod2Bonus, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)

    def test_maxTargetRange(self):
        self.buildTested = 174282
        bonusAttrName = "maxTargetRangeBonus"
        targetAttrName = "maxTargetRange"
        penalize = True
        mod1Bonus = self.testItem1.getAttribute(bonusAttrName)
        mod2Bonus = self.testItem2.getAttribute(bonusAttrName)
        expected = ModifiedAttributeDict()
        expected.original = self.fit.ship.item.attributes
        expected.boost(targetAttrName, mod1Bonus, stackingPenalties = penalize)
        expected.boost(targetAttrName, mod2Bonus, stackingPenalties = penalize)
        actual = self.fit.ship.getModifiedItemAttr(targetAttrName)
        self.assertAlmostEquals(expected[targetAttrName], actual)
