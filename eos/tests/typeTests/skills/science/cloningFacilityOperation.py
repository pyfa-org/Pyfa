from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Cloning Facility Operation"

    # Increases a Clone Vat Bay's maximum clone capacity by 15% per skill level.

    def test_maxJumpClones_shipTitan(self):
        self.buildTested = 0
        attr = "maxJumpClones"
        ship = "Erebus"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=ship)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_maxJumpClones_shipCapitalIndustrial(self):
        self.buildTested = 0
        attr = "maxJumpClones"
        ship = "Rorqual"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=ship)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
