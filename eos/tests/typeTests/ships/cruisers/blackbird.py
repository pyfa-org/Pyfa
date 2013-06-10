from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Blackbird"

    # Caldari Cruiser Skill Bonus:
    # 15% bonus to ECM Target Jammer strength per level

    def test_caldariCruiser_scanGravimetricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM - Phase Inverter I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_scanGravimetricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariCruiser_scanLadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM - White Noise Generator I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_scanLadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariCruiser_scanMagnetometricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM - Multispectral Jammer I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_scanMagnetometricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM Burst I"
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

    def test_caldariCruiser_scanRadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM - Ion Field Projector I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_scanRadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM Burst I"
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
    # 10% bonus to ECM Target Jammer optimal range per level

    def test_caldariCruiser_maxRange_moduleEcm(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "ECM - Phase Inverter I"
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

    def test_caldariCruiser_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "ECCM Projector I"
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
    # 10% bonus to ECM Target Jammer falloff per level

    def test_caldariCruiser_falloff_moduleEcm(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECM - Ion Field Projector I"
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

    def test_caldariCruiser_falloff_moduleOther(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECM Burst I"
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
