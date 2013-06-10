from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Keres"

    # Gallente Frigate Skill Bonus:
    # 5% bonus to remote sensor dampener effectiveness per level

    def test_gallenteFrigate_maxTargetRangeBonus_moduleRemoteSensorDamper(self):
        self.buildTested = 0
        attr = "maxTargetRangeBonus"
        item = "Remote Sensor Dampener I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteFrigate_maxTargetRangeBonus_moduleOther(self):
        self.buildTested = 0
        attr = "maxTargetRangeBonus"
        item = "Remote Sensor Booster I"
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

    def test_gallenteFrigate_scanResolutionBonus_moduleRemoteSensorDamper(self):
        self.buildTested = 0
        attr = "scanResolutionBonus"
        item = "Remote Sensor Dampener I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteFrigate_scanResolutionBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanResolutionBonus"
        item = "Remote Sensor Booster I"
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

    # Gallente Frigate Skill Bonus:
    # 10% reduction in remote sensor dampener capacitor need per level

    def test_gallenteFrigate_capacitorNeed_moduleRemoteSensorDamper(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Remote Sensor Dampener I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteFrigate_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Tracking Link I"
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

    # Electronic Attack Ships Skill Bonus:
    # 10% bonus to warp disruptor range

    def test_electronicAttackShips_maxRange_moduleWarpScrambler(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Warp Scrambler I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_maxRange_moduleWarpScramblerCivilian(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Warp Disruptor"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Stasis Webifier I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Electronic Attack Ships Skill Bonus:
    # 10% reduction in warp disruptor capacitor need per level

    def test_electronicAttackShips_capacitorNeed_moduleWarpScrambler(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Warp Disruptor I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_capacitorNeed_moduleWarpScramblerCivilian(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Warp Disruptor"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Stasis Webifier I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
