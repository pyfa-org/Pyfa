from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Salvaging"

    # 5% increase in chance of salvage retrieval per level.

    def test_accessDifficultyBonus_moduleDataMinerSkillrq(self):
        self.buildTested = 0
        attr = "accessDifficultyBonus"
        item = "Salvager I"
        iLvl = 1
        iIngame = 5.0
        fLvl = 4
        fIngame = 20.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_accessDifficultyBonus_moduleDataMinerNoSkillrq(self):
        self.buildTested = 0
        attr = "accessDifficultyBonus"
        item = "Analyzer I"
        iLvl = 1
        iIngame = 5.0
        fLvl = 4
        fIngame = 5.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
