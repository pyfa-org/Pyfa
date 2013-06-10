from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Jump Drive Calibration"

    # Each skill level grants a 25% increase in maximum jump range.

    def test_jumpDriveRange_ship(self):
        self.buildTested = 0
        attr = "jumpDriveRange"
        ship = "Archon"
        iLvl = 1
        iIngame = 1.25
        fLvl = 4
        fIngame = 2.0
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=ship)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
