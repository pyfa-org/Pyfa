from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Omen Navy Issue"

    # Amarr Cruiser Skill Bonus:
    # 10% bonus to Medium Energy Turret capacitor use per level

    def test_amarrCruiser_capacitorNeed_moduleEnergyWeaponMedium(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Heavy Pulse Laser I"
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
        item = "Dual Heavy Beam Laser I"
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
    # 7.5% bonus to Medium Energy Turret rate of fire per level

    def test_amarrCruiser_speed_moduleEnergyWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Beam Laser I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 0.925
        fLvl = 4
        fIngame = 0.7
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrCruiser_speed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Mega Beam Laser I"
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
