from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Kinetic Shield Compensation"

    # To passive shield hardeners: 5% bonus per skill level to Shield Kinetic resistance

    def test_kineticDamageResistanceBonus_moduleShieldAmplifierSkillrqShieldUpgrades(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Kinetic Deflection Amplifier I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_kineticDamageResistanceBonus_moduleShieldAmplifierSkillrqEngineering(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Basic Kinetic Deflection Amplifier"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_kineticDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Medium Anti-Kinetic Screen Reinforcer I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # To active shield hardeners: 3% bonus per skill level to Shield Kinetic resistance when the modules are not active

    def test_passiveKineticDamageResistanceBonus_moduleShieldHardenerSkillrqTacticalShieldManipulation(self):
        self.buildTested = 0
        attr = "passiveKineticDamageResistanceBonus"
        item = "Ballistic Deflection Field I"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveKineticDamageResistanceBonus_moduleShieldHardenerSkillrqEngineering(self):
        self.buildTested = 0
        attr = "passiveKineticDamageResistanceBonus"
        item = "Civilian Ballistic Deflection Field"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveKineticDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "passiveKineticDamageResistanceBonus"
        item = "Armor Kinetic Hardener I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
