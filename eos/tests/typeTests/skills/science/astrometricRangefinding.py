from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Astrometric Rangefinding"

    # 10% increase to scan probe strength per level.

    def test_baseSensorStrength_chargeScanProbe(self):
        self.buildTested = 0
        attr = "baseSensorStrength"
        item = "Combat Scanner Probe I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
