from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Signal Suppression"
        self.attrs = ("maxTargetRangeBonus", "scanResolutionBonus")

    # 5% bonus to remote sensor dampers' scan resolution and targeting range suppression per skill level.

    def test_sensorDamp_moduleRemoteSensorDamper(self):
        self.buildTested = 0
        item = "Remote Sensor Dampener I"
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

    def test_sensorDamp_moduleOtherSkillrqSenslink(self):
        self.buildTested = 0
        item = "Remote Sensor Booster I"
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
