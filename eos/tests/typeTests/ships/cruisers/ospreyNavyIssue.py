from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Osprey Navy Issue"

    # Caldari Cruiser Skill Bonus:
    # 5% bonus to Assault Missile Launcher rate of fire per level

    def test_caldariCruiser_speed_moduleLauncherMissileAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Assault Missile Launcher I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 5% bonus to Heavy Assault Missile Launcher rate of fire per level

    def test_caldariCruiser_speed_moduleLauncherMissileHeavyAssault(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Assault Missile Launcher I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 5% bonus to Heavy Missile Launcher rate of fire per level

    def test_caldariCruiser_speed_moduleLauncherMissileHeavy(self):
        self.buildTested = 0
        attr = "speed"
        item = "Heavy Missile Launcher I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_speed_moduleLauncherMissileOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Rocket Launcher I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 10% bonus to Heavy Assault Missile velocity per level

    def test_caldariCruiser_maxVelocity_chargeMissileAssault(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Hellfire Assault Missile"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_maxVelocity_chargeMissileAssaultAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Fulmination Javelin Assault Missile"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 10% bonus to Heavy Missile velocity per level

    def test_caldariCruiser_maxVelocity_chargeMissileHeavy(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Widowmaker Heavy Missile"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_maxVelocity_chargeMissileHeavyAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Scourge Fury Heavy Missile"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_maxVelocity_chargeMissileHeavyFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Stalker F.O.F. Heavy Missile I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_maxVelocity_chargeOther(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Flameburst Light Missile"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
