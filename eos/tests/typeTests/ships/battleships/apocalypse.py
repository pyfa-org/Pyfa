from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Apocalypse"

    # Amarr Battleship Skill Bonus:
    # 10% bonus to Large Energy Turret capacitor use per level

    def test_amarrBattleship_capacitorNeed_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Tachyon Beam Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrBattleship_capacitorNeed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual Light Beam Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Battleship Skill Bonus:S
    # 7.5% bonus to Large Energy Turret optimal range per level

    def test_amarrBattleship_maxRange_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Mega Pulse Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrBattleship_maxRange_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Heavy Pulse Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
