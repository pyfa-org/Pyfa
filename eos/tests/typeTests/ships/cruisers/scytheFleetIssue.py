from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Scythe Fleet Issue"

    # Minmatar Cruiser Skill Bonus:
    # 5% bonus to Medium Projectile Turret rate of fire per level

    def test_minmatarCruiser_speed_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "720mm Howitzer Artillery I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_speed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
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

    # Minmatar Cruiser Skill Bonus:
    # 5% bonus to Assault Missile Launcher rate of fire per level

    def test_minmatarCruiser_speed_moduleLauncherMissileAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Assault Missile Launcher I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Cruiser Skill Bonus:
    # 5% bonus to Heavy Assault Missile Launcher rate of fire per level

    def test_minmatarCruiser_speed_moduleLauncherMissileHeavyAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Assault Missile Launcher I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Cruiser Skill Bonus:
    # 5% bonus to Heavy Missile Launcher rate of fire per level

    def test_minmatarCruiser_speed_moduleLauncherMissileHeavy(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Missile Launcher I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_speed_moduleLauncherMissileOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Standard Missile Launcher I"
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
