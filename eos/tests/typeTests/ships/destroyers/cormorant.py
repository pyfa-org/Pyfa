from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Cormorant"

    # Destroyer Skill Bonus:
    # 10% bonus to Small Hybrid Turret tracking speed per level

    def test_destroyers_trackingSpeed_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "125mm Railgun I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_trackingSpeed_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Heavy Ion Blaster I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Destroyer Skill Bonus:
    # 10% bonus to Small Hybrid Turret optimal range per level

    def test_destroyers_maxRange_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Light Neutron Blaster I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_maxRange_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Dual 150mm Railgun I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonuses:
    # Bonus: 50% bonus to optimal range for small hybrid turrets

    def test_static_maxRange_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "75mm Gatling Rail I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "200mm Railgun I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
