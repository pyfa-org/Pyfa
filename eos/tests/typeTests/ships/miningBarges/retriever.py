from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Retriever"

    # Mining Barge Skill Bonus:
    # 3% better yield for Strip Miners per level

    def test_miningBarge_miningAmount_moduleFrequencyMiningLaser(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Modulated Strip Miner II"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.03
        fLvl = 4
        fIngame = 1.12
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_miningBarge_miningAmount_moduleStripMiner(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Strip Miner I"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.03
        fLvl = 4
        fIngame = 1.12
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_miningBarge_miningAmount_moduleIceHarvester(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Ice Harvester I"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.03
        fLvl = 4
        fIngame = 1.12
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_miningBarge_miningAmount_moduleOtherSkillrqDeepCoreMining(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Deep Core Mining Laser I"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_miningBarge_miningAmount_moduleOther(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Gas Cloud Harvester I"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_miningBarge_miningAmount_otherSkillrqMining(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Mining Drone I"
        skill = "Mining Barge"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
