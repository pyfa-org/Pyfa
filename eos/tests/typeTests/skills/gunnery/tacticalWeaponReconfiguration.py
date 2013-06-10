from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Tactical Weapon Reconfiguration"

    # 25-unit reduction in strontium clathrate consumption amount for siege module activation per skill level.

    def test_consumptionQuantity_moduleSiegeModuleSkillrq(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Siege Module I"
        iLvl = 1
        iIngame = 225
        fLvl = 4
        fIngame = 150
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_consumptionQuantity_moduleSiegeModuleNoSkillrq(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Triage Module I"
        iLvl = 1
        iIngame = 500
        fLvl = 4
        fIngame = 500
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_consumptionQuantity_moduleOther(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Jump Portal Generator I"
        iLvl = 1
        iIngame = 500
        fLvl = 4
        fIngame = 500
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
