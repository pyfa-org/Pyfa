from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Imperial Navy Slicer"

    # Amarr Frigate Skill Bonus:
    # 10% bonus to Small Energy Turret optimal range per level

    def test_amarrFrigate_maxRange_moduleEnergyWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Medium Pulse Laser I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_maxRange_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Focused Medium Beam Laser I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Frigate Skill Bonus:
    # 25% bonus to Small Energy Turret damage per level

    def test_amarrFrigate_damageMultiplier_moduleEnergyWeaponSmall(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Dual Light Beam Laser I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.25
        fLvl = 4
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_damageMultiplier_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Heavy Pulse Laser I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
