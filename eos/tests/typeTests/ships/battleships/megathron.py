from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Megathron"

    # Gallente Battleship Skill Bonus:
    # 5% bonus to Large Hybrid Turret damage per level

    def test_gallenteBattleship_damageMultiplier_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "350mm Railgun I"
        skill = "Gallente Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteBattleship_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "75mm Gatling Rail I"
        skill = "Gallente Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Battleship Skill Bonus:
    # 7.5% bonus to Large Hybrid Turret tracking speed per level

    def test_gallenteBattleship_trackingSpeed_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Ion Blaster Cannon I"
        skill = "Gallente Battleship"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteBattleship_trackingSpeed_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Heavy Ion Blaster I"
        skill = "Gallente Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
