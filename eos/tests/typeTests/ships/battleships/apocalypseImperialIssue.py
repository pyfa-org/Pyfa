from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Apocalypse Imperial Issue"

    # Amarr Battleship Skill Bonus:
    # 10% bonus to Large Energy Turret capacitor use per level

    def test_amarrBattleship_capacitorNeed_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual Heavy Beam Laser I"
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
        item = "Gatling Pulse Laser I"
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

    # Amarr Battleship Skill Bonus:
    # 5% maximum Capacitor Capacity per level

    def test_amarrBattleship_capacitorCapacity_ship(self):
        self.buildTested = 0
        attr = "capacitorCapacity"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
