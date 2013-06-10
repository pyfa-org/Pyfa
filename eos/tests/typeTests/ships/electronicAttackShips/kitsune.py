from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Kitsune"

    # Caldari Frigate Skill Bonus:
    # 20% bonus to ECM target jammer strength per level

    def test_caldariFrigate_scanGravimetricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM - Ion Field Projector I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_scanGravimetricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariFrigate_scanLadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM - White Noise Generator I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_scanLadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariFrigate_scanMagnetometricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM - Spatial Destabilizer I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_scanMagnetometricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariFrigate_scanRadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM - Phase Inverter I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_scanRadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM Burst I"
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
    # 10% reduction in ECM target jammers' capacitor need per level

    def test_caldariFrigate_capacitorNeed_moduleEcm(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "ECM - Multispectral Jammer I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "ECM Burst I"
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

    # Electronic Attack Ships Skill Bonus:
    # 10% bonus to ECM target jammer optimal range per level

    def test_electronicAttackShips_maxRange_moduleEcm(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "ECM - Multispectral Jammer I"
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

    def test_electronicAttackShips_falloff_moduleEcm(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECM - Multispectral Jammer I"
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

    def test_electronicAttackShips_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "ECCM Projector I"
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
    # 5% bonus to capacitor capacity per level

    def test_electronicAttackShips_capacitorCapacity_ship(self):
        self.buildTested = 0
        attr = "capacitorCapacity"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
