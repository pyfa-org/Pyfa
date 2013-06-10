from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Deep Core Mining"

    # 20% reduction per skill level in the chance of a damage cloud forming while mining Mercoxit.

    def test_damageCloudChance_moduleDeepCoreMiner(self):
        self.buildTested = 0
        attr = "damageCloudChance"
        item = "Deep Core Mining Laser I"
        iLvl = 1
        iIngame = 0.8
        fLvl = 4
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
