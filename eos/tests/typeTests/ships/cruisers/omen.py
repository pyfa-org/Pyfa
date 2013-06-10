from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Omen"

    # Amarr Cruiser Skill Bonus:
    # 10% bonus to Medium Energy Turret capacitor use per level

    def test_amarrCruiser_capacitorNeed_moduleEnergyWeaponMedium(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Focused Medium Pulse Laser I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrCruiser_capacitorNeed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Mega Pulse Laser I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Cruiser Skill Bonus:
    # 5% bonus to Medium Energy Turret rate of fire per level

    def test_amarrCruiser_speed_moduleEnergyWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "Focused Medium Beam Laser I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrCruiser_speed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Gatling Pulse Laser I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
