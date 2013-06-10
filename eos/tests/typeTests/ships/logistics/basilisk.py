from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Basilisk"

    # Caldari Cruiser Skill Bonus:
    # 150% bonus to Shield Transport range per level

    def test_caldariCruiser_shieldTransferRange_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Medium Shield Transporter I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_shieldTransferRange_moduleShieldTransporterCapital(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Capital Shield Transporter I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_shieldTransferRange_moduleShieldTransporterCivilian(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Civilian Remote Shield Transporter"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 150% bonus to Energy Transfer Array range per level

    def test_caldariCruiser_powerTransferRange_moduleEnergyTransfer(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Large Energy Transfer Array I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_powerTransferRange_moduleEnergyTransferCapital(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Capital Energy Transfer Array I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_powerTransferRange_moduleOther(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Heavy Nosferatu I"
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
    # 20% bonus to Shield Maintenance Bot transfer amount per level
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
        item = "Small Shield Booster I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Logistics Skill Bonus:
    # 15% reduction in Shield Transport capacitor use per level

    def test_logistics_capacitorNeed_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Shield Transporter I"
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

    # Logistics Skill Bonus:
    # 15% reduction in Energy Transfer Array capacitor use per level

    def test_logistics_capacitorNeed_moduleEnergyTransfer(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Energy Transfer Array I"
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

    def test_logistics_capacitorNeed_moduleEnergyTransferCapital(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Capital Energy Transfer Array I"
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
        item = "ECM Burst I"
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
        item = "Micro Shield Transporter I"
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
        item = "Ballistic Control System I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # -50% power need for Energy Transfer Arrays

    def test_static_power_moduleEnergyTransfer(self):
        self.buildTested = 0
        attr = "power"
        item = "Medium Energy Transfer Array I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleEnergyTransferCapital(self):
        self.buildTested = 0
        attr = "power"
        item = "Capital Energy Transfer Array I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleOther(self):
        self.buildTested = 0
        attr = "power"
        item = "Large Proton Smartbomb I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
