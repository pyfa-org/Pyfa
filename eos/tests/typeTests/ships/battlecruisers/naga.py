from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Naga"


    # Battlecruiser Skill Bonus Per Level:
    # 5% bonus to Large Hybrid Turret damage

    def test_battlecruisers_damageMultiplier_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Electron Blaster Cannon I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Light Electron Blaster I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Battlecruiser Skill Bonus Per Level:
    # 10% bonus to Large Hybrid Turret optimal range

    def test_battlecruisers_maxRange_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "425mm Railgun I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_maxRange_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "200mm Railgun I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 95% reduction in the powergrid need of Large Hybrid Turrets

    def test_static_power_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "power"
        item = "Ion Blaster Cannon I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 0.05
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "power"
        item = "Dual 150mm Railgun I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 50% reduction in the CPU need of Large Hybrid Turrets

    def test_static_cpu_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Neutron Blaster Cannon I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Light Electron Blaster I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 50% reduction in the capacitor need of Large Hybrid Turrets

    def test_static_capacitorNeed_moduleHybridWeaponLarge(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual 250mm Railgun I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Heavy Ion Blaster I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
