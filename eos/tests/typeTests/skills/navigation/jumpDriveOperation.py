from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Jump Drive Operation"

    # Each skill level reduces the capacitor need of initiating a jump by 5%.

    def test_jumpDriveCapacitorNeed_ship(self):
        self.buildTested = 0
        attr = "jumpDriveCapacitorNeed"
        ship = "Revelation"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=ship)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
