from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Explosive Shield Compensation"

    # To passive shield hardeners: 5% bonus per skill level to Shield Explosive resistance

    def test_explosiveDamageResistanceBonus_moduleShieldAmplifierSkillrqShieldUpgrades(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Explosion Dampening Amplifier I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_explosiveDamageResistanceBonus_moduleShieldAmplifierSkillrqEngineering(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Basic Explosion Dampening Amplifier"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_explosiveDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Small Anti-Explosive Screen Reinforcer I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # To active shield hardeners: 3% bonus per skill level to Shield Explosive resistance when the modules are not active

    def test_passiveExplosiveDamageResistanceBonus_moduleShieldHardenerSkillrqTacticalShieldManipulation(self):
        self.buildTested = 0
        attr = "passiveExplosiveDamageResistanceBonus"
        item = "Explosion Dampening Field I"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveExplosiveDamageResistanceBonus_moduleShieldHardenerSkillrqEngineering(self):
        self.buildTested = 0
        attr = "passiveExplosiveDamageResistanceBonus"
        item = "Civilian Explosion Dampening Field"
        iLvl = 1
        iIngame = 3.0
        fLvl = 4
        fIngame = 12.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_passiveExplosiveDamageResistanceBonus_moduleOther(self):
        self.buildTested = 0
        attr = "passiveExplosiveDamageResistanceBonus"
        item = "Armor Explosive Hardener I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
