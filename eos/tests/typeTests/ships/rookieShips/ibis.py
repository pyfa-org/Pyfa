from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Ibis"

    # Special Ability:
    # 10% bonus hybrid turret optimal range per skill level
    # Description is wrong, it uses Caldari Frigate as boost skill

    def test_caldariFrigate_maxRange_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "75mm Gatling Rail I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_maxRange_moduleHybridWeaponOtherl(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Dual 150mm Railgun I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
