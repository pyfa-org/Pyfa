from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Signature Focusing"

    # 5% bonus to target painter modules' signature radius multiplier per skill level.

    def test_signatureRadiusBonus_moduleTargetPainter(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Target Painter I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_signatureRadiusBonus_moduleOther(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "1MN MicroWarpdrive I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
