from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Hoarder"

    # Minmatar Industrial Skill Bonus:
    # 5% Bonus Cargo Capacity per skill level

    def test_minmatarIndustrial_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        skill = "Minmatar Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Industrial Skill Bonus:
    # 5% Bonus Max Velocity per skill level

    def test_minmatarIndustrial_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Minmatar Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
