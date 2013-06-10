from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Kinetic Armor Compensation"

    # To passive armor hardeners: 5% bonus per skill level to Armor Kinetic resistance

    def test_kineticDamageResistanceBonus_moduleArmorCoatingSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Magnetic Plating I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_kineticDamageResistanceBonus_moduleArmorCoatingSkillrqMechanic(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Basic Magnetic Plating"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_kineticDamageResistanceBonus_moduleArmorPlatinEnergized(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
        item = "Energized Magnetic Membrane I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_kineticDamageResistanceBonus_moduleOtherSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "kineticDamageResistanceBonus"
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

    # To active armor hardeners: 3% bonus per skill level to Armor Kinetic resistance when the modules are not active

    def test_passiveKineticDamageResistanceBonus_moduleArmorHardener(self):
        self.buildTested = 0
        attr = "passiveKineticDamageResistanceBonus"
        item = "Armor Kinetic Hardener I"
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
        item = "Ballistic Deflection Field I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
