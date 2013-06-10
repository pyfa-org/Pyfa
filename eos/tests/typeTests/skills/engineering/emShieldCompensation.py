from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "EM Shield Compensation"

    # To passive shield hardeners: 5% bonus per skill level to Shield EM resistance

    def test_emDamageResistanceBonus_moduleShieldAmplifierSkillrqShieldUpgrades(self):
        self.buildTested = 0
        attr = "emDamageResistanceBonus"
        item = "Magnetic Scattering Amplifier I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_emDamageResistanceBonus_moduleShieldAmplifierSkillrqEngineering(self):
        self.buildTested = 0
        attr = "emDamageResistanceBonus"
        item = "Basic Magnetic Scattering Amplifier"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_emDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "emDamageResistanceBonus"
        item = "Large Anti-EM Pump I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # To active shield hardeners: 3% bonus per skill level to Shield EM resistance when the modules are not active

    def test_passiveEmDamageResistanceBonus_moduleShieldHardenerSkillrqTacticalShieldManipulation(self):
        self.buildTested = 0
        attr = "passiveEmDamageResistanceBonus"
        item = "Photon Scattering Field I"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveEmDamageResistanceBonus_moduleShieldHardenerSkillrqEngineering(self):
        self.buildTested = 0
        attr = "passiveEmDamageResistanceBonus"
        item = "Civilian Photon Scattering Field"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveEmDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "passiveEmDamageResistanceBonus"
        item = "Armor EM Hardener I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
