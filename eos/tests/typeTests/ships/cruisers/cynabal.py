from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Cynabal"

    # Minmatar Cruiser Skill Bonus:
    # 10% bonus to Medium Projectile Turret damage per level

    def test_minmatarCruiser_damageMultiplier_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "720mm Howitzer Artillery I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "150mm Light AutoCannon I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to Medium Projectile Turret falloff per level

    def test_gallenteCruiser_falloff_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "falloff"
        item = "425mm AutoCannon I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_falloff_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Dual 425mm AutoCannon I"
        skill = "Gallente Cruiser"
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
    # 25% bonus to Medium Projectile Turret rate of fire

    def test_static_speed_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "Dual 180mm AutoCannon I"
        ship_other = "Thorax"
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
        item = "200mm AutoCannon I"
        ship_other = "Thorax"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
