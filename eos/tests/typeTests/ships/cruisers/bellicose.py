from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Bellicose"

    # Minmatar Cruiser Skill Bonus:
    # 5% bonus to Medium Projectile Turret Rate of Fire per skill level

    def test_minmatarCruiser_speed_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "220mm Vulcan AutoCannon I"
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
        item = "280mm Howitzer Artillery I"
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
    # 7.5% bonus to target painter effectiveness per skill level

    def test_minmatarCruiser_signatureRadiusBonus_moduleTargetPainter(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Target Painter I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_signatureRadiusBonus_other(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Warrior TP-300"
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
