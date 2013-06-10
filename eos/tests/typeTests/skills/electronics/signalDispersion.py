from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Signal Dispersion"

    # 5% bonus to strength of all ECM jammers per skill level.

    def test_scanSensorStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
        item = "ECM - Multispectral Jammer I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        for type in sensorTypes:
            attr = "scan{0}StrengthBonus".format(type)
            iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
            fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
            dIngame = fIngame / iIngame
            dEos = fEos / iEos
            self.assertAlmostEquals(dEos, dIngame)

    def test_scanSensorStrengthBonus_moduleEcmBurst(self):
        self.buildTested = 0
        sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
        item = "ECM Burst I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        for type in sensorTypes:
            attr = "scan{0}StrengthBonus".format(type)
            iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
            fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
            dIngame = fIngame / iIngame
            dEos = fEos / iEos
            self.assertAlmostEquals(dEos, dIngame)

    def test_scanSensorStrengthBonus_moduleOther(self):
        self.buildTested = 0
        sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
        item = "Remote ECM Burst I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        for type in sensorTypes:
            attr = "scan{0}StrengthBonus".format(type)
            iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
            fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
            dIngame = fIngame / iIngame
            dEos = fEos / iEos
            self.assertAlmostEquals(dEos, dIngame)
