from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Cloaking"

    # 10% reduction in targeting delay after uncloaking per skill level.

    def test_cloakingTargetingDelay_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cloakingTargetingDelay"
        item = "Prototype Cloaking Device I"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
