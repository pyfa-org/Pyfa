from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Scythe"

    # Minmatar Cruiser Skill Bonus:
    # 20% bonus to mining laser yield per level

    def test_minmatarCruiser_miningAmount_moduleMiningLaser(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Miner I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_miningAmount_moduleMiningLaserDeepCore(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Deep Core Mining Laser I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_miningAmount_moduleOther(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Gas Cloud Harvester I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_miningAmount_other(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Mining Drone I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Cruiser Skill Bonus:
    # 3.5% bonus to tracking links per level

    def test_minmatarCruiser_maxRangeBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Link I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.035
        fLvl = 4
        fIngame = 1.14
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_maxRangeBonus_moduleOther(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Disruptor I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_falloffBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Link I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.035
        fLvl = 4
        fIngame = 1.14
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_falloffBonus_moduleOther(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Computer I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_trackingSpeedBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Link I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 1.035
        fLvl = 4
        fIngame = 1.14
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_trackingSpeedBonus_moduleOther(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Enhancer I"
        skill = "Minmatar Cruiser"
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
    # 500% bonus to range of tracking links

    def test_static_maxRange_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Tracking Link I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Remote Sensor Booster I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
