from eos.tests import TestBase
from eos.types import Drone
from eos import db

class Test(TestBase):
    def test_increase(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.increaseItemAttr("speed", 1302)
        self.assertEquals(originalSpeed + 1302, d.itemModifiedAttributes["speed"])

    def test_multiply(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.multiplyItemAttr("speed", 2.35)
        self.assertAlmostEquals(originalSpeed * 2.35, d.itemModifiedAttributes["speed"])

    def test_boost(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.boostItemAttr("speed", 20)
        self.assertAlmostEquals(originalSpeed * 1.20, d.itemModifiedAttributes["speed"])

    def test_stackingPenalizedMultiply(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.multiplyItemAttr("speed", 2.35, stackingPenalties = True) #Should get penalties
        d.multiplyItemAttr("speed", 2.6, stackingPenalties = True) #Shouldn't get penalties
        d.multiplyItemAttr("speed", 0.4, stackingPenalties = True) #Shouldn't get penalties
        d.multiplyItemAttr("speed", 0.6, stackingPenalties = True) #Should get penalties
        self.assertAlmostEquals(originalSpeed * (1 + -0.4* 0.86911998) * 0.4 * (1 + 1.35 * 0.86911998) *  (1 + 1.6),
                                d.itemModifiedAttributes["speed"], 2)

    def test_stackingPenaltyMultiplyGroups(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.multiplyItemAttr("speed", 2.1, stackingPenalties = True, penaltyGroup = "test1") #Shouldn't get penaltied
        d.multiplyItemAttr("speed", 2.5, stackingPenalties = True, penaltyGroup = "test2") #Should get penaltied
        d.multiplyItemAttr("speed", 2.7, stackingPenalties = True, penaltyGroup = "test2") #Shouldn't get penaltied
        d.multiplyItemAttr("speed", 1.6, stackingPenalties = True, penaltyGroup = "test1") #Should get penaltied
        self.assertAlmostEqual(originalSpeed * 2.1 * 2.7 * (1 + 1.5 * 0.86911998) * (1 + 0.6 * 0.86911998),
                               d.itemModifiedAttributes["speed"], 2)

    def test_stackingPenalizedBoost(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.boostItemAttr("speed", 35, stackingPenalties = True) #Should get penalties
        d.boostItemAttr("speed", 60, stackingPenalties = True) #Shouldn't get penalties
        d.boostItemAttr("speed", -40, stackingPenalties = True) #Should get penalties
        d.boostItemAttr("speed", -60, stackingPenalties = True) #Shouldn't get penalties
        self.assertAlmostEquals(originalSpeed * (1 + 0.35 * 0.86911998) * 1.6 * (1 - 0.6) * (1 - 0.4 * 0.86911998),
                                d.itemModifiedAttributes["speed"], 2)

    def test_stackingPenaltyBoostGroups(self):
        d = Drone(db.getItem("Hobgoblin I"))
        originalSpeed = d.itemModifiedAttributes["speed"]
        d.boostItemAttr("speed", 10, stackingPenalties = True, penaltyGroup = "test1") #Should get penaltied
        d.boostItemAttr("speed", 50, stackingPenalties = True, penaltyGroup = "test2") #Should get penaltied
        d.boostItemAttr("speed", 70, stackingPenalties = True, penaltyGroup = "test2") #Shouldn't get penaltied
        d.boostItemAttr("speed", 60, stackingPenalties = True, penaltyGroup = "test1") #Shouldn't get penaltied
        self.assertAlmostEqual(originalSpeed * (1 + 0.10 * 0.86911998) * (1 + 0.5 * 0.86911998) * 1.7 * 1.6,
                               d.itemModifiedAttributes["speed"], 2)
