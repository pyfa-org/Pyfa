from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Jump Portal Generation"

    # 10% reduced material cost for jump portal activation per level.

    def test_consumptionQuantity_moduleJumpPortalGenerator(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Jump Portal Generator I"
        iLvl = 1
        iIngame = 450.0
        fLvl = 4
        fIngame = 300.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_consumptionQuantity_moduleOther(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Cynosural Field Generator I"
        iLvl = 1
        iIngame = 500.0
        fLvl = 4
        fIngame = 500.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
