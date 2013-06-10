from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Occator"

    # Gallente Industrial Skill Bonus:
    # +5% cargo capacity per level

    def test_gallenteIndustrial_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        skill = "Gallente Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Industrial Skill Bonus:
    # +5% velocity per level

    def test_gallenteIndustrial_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Gallente Industrial"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Transport Ships Skill Bonus:
    # +5% armor repairer boost amount per level

    def test_transportShips_armorDamageAmount_moduleArmorRepairer(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Small Armor Repairer I"
        skill = "Transport Ships"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_transportShips_armorDamageAmount_moduleArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Capital Armor Repairer I"
        skill = "Transport Ships"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_transportShips_armorDamageAmount_moduleArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Civilian Armor Repairer"
        skill = "Transport Ships"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_transportShips_armorDamageAmount_moduleOther(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Large Remote Armor Repair System I"
        skill = "Transport Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Transport Ships Skill Bonus:
    # +5% bonus to armor HP per level

    def test_transportShips_armorHP_ship(self):
        self.buildTested = 0
        attr = "armorHP"
        skill = "Transport Ships"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # +2 warp strengthv

    def test_static_warpScrambleStatus_ship(self):
        self.buildTested = 0
        attr = "warpScrambleStatus"
        ingame = -2.0
        eos = self.getShipAttr(attr, ship=self.ship)
        self.assertAlmostEquals(eos, ingame)
