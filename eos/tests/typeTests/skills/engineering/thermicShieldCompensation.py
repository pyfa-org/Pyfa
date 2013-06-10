from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Thermic Shield Compensation"

    # To passive shield hardeners: 5% bonus per skill level to Shield Thermal resistance

    def test_thermalDamageResistanceBonus_moduleShieldAmplifierSkillrqShieldUpgrades(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Heat Dissipation Amplifier I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_thermalDamageResistanceBonus_moduleShieldAmplifierSkillrqEngineering(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Basic Heat Dissipation Amplifier"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_thermalDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "thermalDamageResistanceBonus"
        item = "Small Anti-Thermic Pump I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # To active shield hardeners: 3% bonus per skill level to Shield Thermal resistance when the modules are not active

    def test_passiveThermicDamageResistanceBonus_moduleShieldHardenerSkillrqTacticalShieldManipulation(self):
        self.buildTested = 0
        attr = "passiveThermicDamageResistanceBonus"
        item = "Heat Dissipation Field I"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveThermicDamageResistanceBonus_moduleShieldHardenerSkillrqEngineering(self):
        self.buildTested = 0
        attr = "passiveThermicDamageResistanceBonus"
        item = "Civilian Heat Dissipation Field"
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
