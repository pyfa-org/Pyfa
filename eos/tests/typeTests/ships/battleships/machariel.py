from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Machariel"

    # Minmatar Battleship Skill Bonus:
    # 5% bonus to Large Projectile Turret damage per level

    def test_minmatarBattleship_damageMultiplier_moduleProjectileWeaponLarge(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "1400mm Howitzer Artillery I"
        skill = "Minmatar Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarBattleship_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "220mm Vulcan AutoCannon I"
        skill = "Minmatar Battleship"
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
    # 10% bonus to Large Projectile Turret falloff per level

    def test_gallenteBattleship_falloff_moduleProjectileWeaponLarge(self):
        self.buildTested = 0
        attr = "falloff"
        item = "800mm Repeating Artillery I"
        skill = "Gallente Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteBattleship_falloff_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "falloff"
        item = "425mm AutoCannon I"
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

    # Special Ability:
    # 25% bonus to Large Projectile Turret rate of fire

    def test_static_speed_moduleProjectileWeaponLarge(self):
        self.buildTested = 0
        attr = "speed"
        item = "Dual 425mm AutoCannon I"
        ship_other = "Abaddon"
        iIngame = 1.0
        fIngame = 0.75
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_speed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "650mm Artillery Cannon I"
        ship_other = "Abaddon"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
