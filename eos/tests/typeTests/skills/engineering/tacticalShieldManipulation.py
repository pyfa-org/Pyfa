from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Tactical Shield Manipulation"

    # Reduces the chance of damage penetrating the shield when it falls below 25% by 5% per skill level, with 0% chance at level 5.

    def test_shieldUniformity(self):
        self.buildTested = 0
        attr = "shieldUniformity"
        iLvl = 1
        iIngame = 0.8
        fLvl = 4
        fIngame = 0.95
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl))
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl))
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
