from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Frequency Modulation"

    # 10% bonus to falloff for ECM per skill level.

    def test_falloff_moduleEcm(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECM - Phase Inverter I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus: 10% bonus to falloff for ECM Burst per skill level.

    def test_falloff_moduleEcmBurst(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECM Burst I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_falloff_moduleOtherSkillrqElectronicWarfare(self):
        self.buildTested = 0
        attr = "falloff"
        item = "ECCM Projector I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # 10% bonus to falloff for Remote Sensor Dampeners per skill level.

    def test_falloff_moduleRemoteSensorDamper(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Remote Sensor Dampener I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_falloff_moduleOtherSkillrqSensorLinking(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Remote Sensor Booster I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # 10% bonus to falloff for Tracking Disruptors per skill level.

    def test_falloff_moduleTrackingDisruptor(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Tracking Disruptor I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # 10% bonus to falloff for Target Painters per skill level.

    def test_falloff_moduleTargetPainter(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Target Painter I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
