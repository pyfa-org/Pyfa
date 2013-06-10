from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Noctis"

    # ORE Industrial Skill Bonus:
    # 5% bonus to Tractor Beam cycle time per level

    def test_oreIndustrial_duration_moduleTractorBeamSkillrqGraviton(self):
        self.buildTested = 0
        attr = "duration"
        item = "Small Tractor Beam I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_oreIndustrial_duration_moduleOther(self):
        self.buildTested = 0
        attr = "duration"
        item = "Passive Targeter I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # ORE Industrial Skill Bonus:
    # 5% bonus to Salvager cycle time per level

    def test_oreIndustrial_duration_moduleDataMinerSkillrqSalvaging(self):
        self.buildTested = 0
        attr = "duration"
        item = "Salvager I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_oreIndustrial_duration_moduleDataMinerSkillrqOther(self):
        self.buildTested = 0
        attr = "duration"
        item = "Analyzer I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # ORE Industrial Skill Bonus:
    # 60% bonus to Tractor Beam range per level

    def test_oreIndustrial_maxRange_moduleTractorBeamSkillrqGraviton(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Small Tractor Beam I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 1.6
        fLvl = 4
        fIngame = 3.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_oreIndustrial_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "200mm Railgun I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # ORE Industrial Skill Bonus:
    # 60% bonus to Tractor Beam velocity per level

    def test_oreIndustrial_maxTractorVelocity_moduleTractorBeamSkillrqGraviton(self):
        self.buildTested = 0
        attr = "maxTractorVelocity"
        item = "Small Tractor Beam I"
        skill = "ORE Industrial"
        iLvl = 1
        iIngame = 1.6
        fLvl = 4
        fIngame = 3.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
