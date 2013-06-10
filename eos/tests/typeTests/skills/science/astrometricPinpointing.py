from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Astrometric Pinpointing"

    # Reduces maximum scan deviation by 10% per level.

    def test_baseMaxScanDeviation_chargeScanProbe(self):
        self.buildTested = 0
        attr = "baseMaxScanDeviation"
        item = "Core Scanner Probe I"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
