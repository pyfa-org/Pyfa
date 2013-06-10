from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Mining Upgrades"

    # 5% reduction per skill level in CPU penalty of mining upgrade modules.

    def test_cpuPenaltyPercent_moduleMiningUpgrade(self):
        self.buildTested = 0
        attr = "cpuPenaltyPercent"
        item = "Mining Laser Upgrade I"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
