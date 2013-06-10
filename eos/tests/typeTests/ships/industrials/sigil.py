from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Sigil"

    # Amarr Industrial Skill Bonus:
    # 5% Bonus Cargo Capacity per skill level

    def test_amarrIndustrial_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        skill = "Amarr Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Industrial Skill Bonus:
    # 5% Bonus Max Velocity per skill level

    def test_amarrIndustrial_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Amarr Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
