from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Raptor"

    # Caldari Frigate Skill Bonus:
    # 5% bonus to Small Hybrid Turret Damage per level

    def test_caldariFrigate_damageMultiplier_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "75mm Gatling Rail I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Dual 150mm Railgun I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Frigate Skill Bonus:
    # 10% bonus to Small Hybrid Turret optimal range per level

    def test_caldariFrigate_maxRange_moduleHybridWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Light Neutron Blaster I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_maxRange_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Heavy Ion Blaster I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Interceptor Skill Bonus:
    # 15% reduction in MicroWarpdrive signature radius penalty per level

    def test_interceptors_signatureRadiusBonus_moduleAfterburnerSkillrqHighSpeedManeuvering(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "1MN MicroWarpdrive I"
        skill = "Interceptors"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interceptors_signatureRadiusBonus_moduleOther(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Inertia Stabilizers I"
        skill = "Interceptors"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Interceptor Skill Bonus:
    # 5% bonus to Warp Scrambler and Warp Disruptor range per level

    def test_interceptors_maxRange_moduleWarpScramblerSkillrqPropJamming(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Warp Scrambler I"
        skill = "Interceptors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interceptors_maxRange_moduleWarpScramblerNoSkillrqPropJamming(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Warp Disruptor"
        skill = "Interceptors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interceptors_maxRange_moduleOtherSkillrqPropJamming(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Stasis Webifier I"
        skill = "Interceptors"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role bonus:
    # 80% reduction in Propulsion Jamming systems activation cost

    def test_static_capacitorNeed_moduleStasisWebSkillrqPropulsionJamming(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Stasis Webifier I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleStasisWebNoSkillrqPropulsionJamming(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Stasis Webifier"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleWarpScramblerSkillrqPropulsionJamming(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Warp Scrambler I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleWarpScramblerNoSkillrqPropulsionJamming(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Warp Disruptor"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Quad Light Beam Laser I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
