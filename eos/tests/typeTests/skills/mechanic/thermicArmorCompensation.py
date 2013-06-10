from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Thermic Armor Compensation"

    # To passive armor hardeners: 5% bonus per skill level to Armor Thermal resistance

    def test_thermalDamageResistanceBonus_moduleArmorCoatingSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Thermic Plating I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_thermalDamageResistanceBonus_moduleArmorCoatingSkillrqMechanic(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Basic Thermic Plating"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_thermalDamageResistanceBonus_moduleArmorPlatinEnergized(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Energized Thermic Membrane I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_thermalDamageResistanceBonus_moduleOtherSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Armor Thermic Hardener I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # To active armor hardeners: 3% bonus per skill level to Armor Thermal resistance when the modules are not active

    def test_passiveThermicDamageResistanceBonus_moduleArmorHardener(self):
        self.buildTested = 0
        attr = "passiveThermicDamageResistanceBonus"
        item = "Armor Thermic Hardener I"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveThermicDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "passiveThermicDamageResistanceBonus"
        item = "Heat Dissipation Field I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
