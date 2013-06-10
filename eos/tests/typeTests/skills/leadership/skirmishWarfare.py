from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Skirmish Warfare"

    # Grants a 2% bonus to fleet members' agility per skill level.

    def test_agility_fleetShip(self):
        self.buildTested = 0
        attr = "agility"
        iLvl = 1
        iIngame = 0.98
        fLvl = 4
        fIngame = 0.92
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), gang=True)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), gang=True)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_agility_fleetSubsystem(self):
        self.buildTested = 0
        attr = "agility"
        item = "Tengu Propulsion - Gravitational Capacitor"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), gang=True)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), gang=True)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
