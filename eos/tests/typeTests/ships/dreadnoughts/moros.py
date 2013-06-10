from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Moros"

    # Gallente Dreadnought Skill Bonus:
    # 5% bonus to Capital Hybrid Turret damage per level

    def test_gallenteDreadnought_damageMultiplier_moduleHybridWeaponCapital(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Dual 1000mm Railgun I"
        skill = "Gallente Dreadnought"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteDreadnought_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Neutron Blaster Cannon I"
        skill = "Gallente Dreadnought"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Dreadnought Skill Bonus:
    # 5% bonus to Capital Hybrid Turret damage per level

    def test_gallenteDreadnought_speed_moduleHybridWeaponCapital(self):
        self.buildTested = 0
        attr = "speed"
        item = "Ion Siege Blaster Cannon I"
        skill = "Gallente Dreadnought"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteDreadnought_speed_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Electron Blaster I"
        skill = "Gallente Dreadnought"
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
