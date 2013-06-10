from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Electronic Warfare Drone Interfacing"

    # 3000m drone control range bonus per level.

    def test_droneControlRange(self):
        self.buildTested = 0
        attr = "droneControlRange"
        iLvl = 1
        iIngame = 3000
        fLvl = 4
        fIngame = 12000
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl))
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
