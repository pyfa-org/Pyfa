from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Naglfar"

    # Minmatar Dreadnought Skill Bonus:
    # 5% bonus to Capital Projectile damage per level

    def test_minmatarDreadnought_damageMultiplier_moduleProjectileWeaponCapital(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "6x2500mm Repeating Artillery I"
        skill = "Minmatar Dreadnought"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarDreadnought_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "125mm Gatling AutoCannon I"
        skill = "Minmatar Dreadnought"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Dreadnought Skill Bonus:
    # 5% bonus to Capital Projectile rate of fire per level

    def test_minmatarDreadnought_speed_moduleProjectileWeaponCapital(self):
        self.buildTested = 0
        attr = "speed"
        item = "Quad 3500mm Siege Artillery I"
        skill = "Minmatar Dreadnought"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarDreadnought_speed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "1400mm Howitzer Artillery I"
        skill = "Minmatar Dreadnought"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Advanced Spaceship Command Skill Bonus:
    # 5% Bonus to the agility of ship per skill level
    # Moved from Advanced Spaceship Command skill tests, not listed as bonus of ship

    def test_advancedSpaceshipCommand_agility_ship(self):
        self.buildTested = 0
        attr = "agility"
        skill = "Advanced Spaceship Command"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
