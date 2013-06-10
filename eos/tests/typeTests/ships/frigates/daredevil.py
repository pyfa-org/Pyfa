from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Daredevil"

    # Gallente Frigate Skill Bonus:
    # 10% bonus to Small Hybrid Turret falloff per level

    def test_gallenteFrigate_falloff_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Light Neutron Blaster I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteFrigate_falloff_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "falloff"
        item = "200mm Railgun I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Frigate Skill Bonus:
    # 10% bonus to the velocity factor of stasis webifiers per level

    def test_minmatarFrigate_speedFactor_moduleStasisWeb(self):
        self.buildTested = 0
        attr = "speedFactor"
        item = "Stasis Webifier I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_speedFactor_moduleStasisWebCivilian(self):
        self.buildTested = 0
        attr = "speedFactor"
        item = "Civilian Stasis Webifier"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_speedFactor_moduleOther(self):
        self.buildTested = 0
        attr = "speedFactor"
        item = "1MN MicroWarpdrive I"
        skill = "Minmatar Frigate"
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
    # 200% bonus to Small Hybrid Turret damage

    def test_static_damageMultiplier_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "150mm Railgun I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 3.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Heavy Neutron Blaster I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
