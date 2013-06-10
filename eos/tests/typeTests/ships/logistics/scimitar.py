from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Scimitar"

    # Minmatar Cruiser Skill Bonus:
    # 150% bonus to Tracking Link range per level

    def test_minmatarCruiser_maxRange_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Tracking Link I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Remote Sensor Dampener I"
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
    # 150% bonus to Shield Transport range per level

    def test_minmatarCruiser_shieldTransferRange_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Medium Shield Transporter I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_shieldTransferRange_moduleShieldTransporterCapital(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Capital Shield Transporter I"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarCruiser_shieldTransferRange_moduleShieldTransporterCivilian(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Civilian Remote Shield Transporter"
        skill = "Minmatar Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Cruiser Skill Bonus:
    # 20% bonus to Shield Maintenance Bot transport amount per level
    # Actually static 100% bonus, anyway cruiser skill must be at V level

    def test_static_shieldBonus_droneLogistics(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Medium Shield Maintenance Bot I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_shieldBonus_other(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Large Shield Booster I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Logistics Skill Bonus:
    # 10% bonus to Tracking Link efficiency per level

    def test_logistics_maxRangeBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_maxRangeBonus_moduleOther(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Enhancer I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_falloffBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_falloffBonus_moduleOther(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Computer I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_trackingSpeedBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_trackingSpeedBonus_moduleOther(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Disruptor I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Logistics Skill Bonus:
    # 15% reduction in Shield Transport capacitor use per level

    def test_logistics_capacitorNeed_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Small Shield Transporter I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleShieldTransporterCapital(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Capital Shield Transporter I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleShieldTransporterCivilian(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Remote Shield Transporter"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Induced Ion Field ECM I"
        skill = "Logistics"
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
    # -50% CPU need for Shield Transporters

    def test_static_cpu_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Large Shield Transporter I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleShieldTransporterCapital(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Capital Shield Transporter I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleShieldTransporterCivilian(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Civilian Remote Shield Transporter"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleOther(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Damage Control I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
