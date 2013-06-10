from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Imicus"

    # Gallente Frigate Skill Bonus:
    # 5% bonus to drone range per level

    def test_gallenteFrigate_droneControlRange_ship(self):
        self.buildTested = 0
        attr = "droneControlRange"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Frigate Skill Bonus:
    # 5% increase to scan strength of probes per level

    def test_gallenteFrigate_baseSensorStrength_chargeScannerProbe(self):
        self.buildTested = 0
        attr = "baseSensorStrength"
        item = "Core Scanner Probe I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Frigate Skill Bonus:
    # 5% bonus to survey probe flight time per level

    def test_gallenteFrigate_explosionDelay_chargeSurveyProbe(self):
        self.buildTested = 0
        attr = "explosionDelay"
        item = "Discovery Survey Probe I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteFrigate_explosionDelay_chargeOther(self):
        self.buildTested = 0
        attr = "explosionDelay"
        item = "Core Scanner Probe I"
        skill = "Gallente Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
