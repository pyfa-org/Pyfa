from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Hyena"

    # Minmatar Frigate Skill Bonus:
    # 5% increase to MicroWarpdrive capacitor bonus per level

    def test_minmatarFrigate_capacitorCapacityMultiplier_moduleAfterburnerSkillrqHSM(self):
        self.buildTested = 0
        attr = "capacitorCapacityMultiplier"
        item = "1MN MicroWarpdrive II"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 0.88
        fLvl = 4
        fIngame = 1.03
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_capacitorCapacityMultiplier_moduleAfterburnerSkillrqAB(self):
        self.buildTested = 0
        attr = "capacitorCapacityMultiplier"
        item = "1MN Afterburner I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Frigate Skill Bonus:
    # 7.5% bonus to effectiveness of target painters per level

    def test_minmatarFrigate_signatureRadiusBonus_moduleTargetPainter(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Target Painter I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_signatureRadiusBonus_moduleOther(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
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

    # Electronic Attack Ships Skill Bonus:
    # 20% bonus to stasis webifier range per level

    def test_electronicAttackShips_maxRange_moduleStasisWeb(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Stasis Webifier I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_maxRange_moduleStasisWebCivilian(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Stasis Webifier"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Warp Disruptor I"
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
    # 3% reduction in signature radius per level

    def test_electronicAttackShips_signatureRadius_ship(self):
        self.buildTested = 0
        attr = "signatureRadius"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 0.97
        fLvl = 4
        fIngame = 0.88
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
