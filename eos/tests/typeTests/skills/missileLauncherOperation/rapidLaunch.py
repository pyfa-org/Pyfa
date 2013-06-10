from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Rapid Launch"

    # 3% bonus to missile launcher rate of fire per level.

    def test_speed_moduleLauncherMissileRocket(self):
        self.buildTested = 0
        attr = "speed"
        item = "Rocket Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileStandard(self):
        self.buildTested = 0
        attr = "speed"
        item = "Standard Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileStandardNoSkillrqMissileOp(self):
        self.buildTested = 0
        attr = "speed"
        item = "Civilian Standard Missile Launcher"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Assault Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileHeavyAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Assault Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileHeavy(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileSiege(self):
        self.buildTested = 0
        attr = "speed"
        item = "Siege Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileCruise(self):
        self.buildTested = 0
        attr = "speed"
        item = "Cruise Missile Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleLauncherMissileCitadel(self):
        self.buildTested = 0
        attr = "speed"
        item = "Citadel Torpedo Launcher I"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_speed_moduleOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Dual 150mm Railgun I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
