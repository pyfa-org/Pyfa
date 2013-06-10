from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Rapid Firing"

    # 4% bonus per skill level to weapon turret rate of fire.

    def test_speed_moduleEnergyWeapon(self):
        self.buildTested = 0
        attr = "speed"
        item = "Medium Pulse Laser I"
        iLvl = 1
        iIngame = 0.96
        fLvl = 4
        fIngame = 0.84
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleHybridWeapon(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Neutron Blaster I"
        iLvl = 1
        iIngame = 0.96
        fLvl = 4
        fIngame = 0.84
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleProjectileWeapon(self):
        self.buildTested = 0
        attr = "speed"
        item = "220mm Vulcan AutoCannon I"
        iLvl = 1
        iIngame = 0.96
        fLvl = 4
        fIngame = 0.84
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Assault Missile Launcher I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
