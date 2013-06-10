from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Information Warfare"

    # Grants a 2% bonus to fleet members' targeting range per skill level.

    def test_maxTargetRange_fleetShip(self):
        self.buildTested = 0
        attr = "maxTargetRange"
        iLvl = 1
        iIngame = 1.02
        fLvl = 4
        fIngame = 1.08
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), gang=True)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), gang=True)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_maxTargetRange_fleetSubsystem(self):
        self.buildTested = 0
        attr = "maxTargetRange"
        item = "Loki Electronics - Emergent Locus Analyzer"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), gang=True)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), gang=True)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
