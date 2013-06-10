from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Scout Drone Operation"

    # Bonus: drone control range increased by 5000 meters per skill level.

    def test_droneControlRange(self):
        self.buildTested = 0
        attr = "droneControlRange"
        iLvl = 1
        iIngame = 5000
        fLvl = 4
        fIngame = 20000
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl))
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
