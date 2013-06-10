from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Turret Destabilization"
        self.attrs = ("maxRangeBonus", "falloffBonus", "trackingSpeedBonus")

    # 5% bonus to Tracking Disruptor modules' tracking speed, optimal range and falloff disruption per skill level.

    def test_turretDisruption_moduleTrackingDisruptor(self):
        self.buildTested = 0
        item = "Tracking Disruptor I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        for attr in self.attrs:
            iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
            fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
            dIngame = fIngame / iIngame
            dEos = fEos / iEos
            self.assertAlmostEquals(dEos, dIngame)

    def test_turretDisruption_moduleOther(self):
        self.buildTested = 0
        item = "Tracking Link I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        for attr in self.attrs:
            iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
            fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
            dIngame = fIngame / iIngame
            dEos = fEos / iEos
            self.assertAlmostEquals(dEos, dIngame)
