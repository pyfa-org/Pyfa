from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.skill = "Explosive Armor Compensation"

    # To passive armor hardeners: 5% bonus per skill level to Armor Explosive resistance

    def test_explosiveDamageResistanceBonus_moduleArmorCoatingSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Reactive Plating I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_explosiveDamageResistanceBonus_moduleArmorCoatingSkillrqMechanic(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Basic Reactive Plating"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_explosiveDamageResistanceBonus_moduleArmorPlatinEnergized(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
        item = "Energized Reactive Membrane I"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_explosiveDamageResistanceBonus_moduleOtherSkillrqHullUpgrades(self):
        self.buildTested = 0
        attr = "explosiveDamageResistanceBonus"
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

    # To active armor hardeners: 3% bonus per skill level to Armor Explosive resistance when the modules are not active

    def test_passiveExplosiveDamageResistanceBonus_moduleArmorHardener(self):
        self.buildTested = 0
        attr = "passiveExplosiveDamageResistanceBonus"
        item = "Armor Explosive Hardener I"
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
        item = "Explosion Dampening Field I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl))
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl))
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
