from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Reaper"

    # Special Ability:
    # 5% bonus to velocity per skill level
    # Description is wrong, it uses Minmatar Frigate as boost skill

    def test_minmatarFrigate_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
