from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Guardian-Vexor"

    # Gallente Cruiser Skill Bonus:
    # 5% bonus to Medium Hybrid Turret damage per level

    def test_gallenteCruiser_damageMultiplier_moduleHybridWeaponMedium(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Heavy Neutron Blaster I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Ion Blaster Cannon I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # +1 extra Drone controlled per level

    def test_gallenteCruiser_maxActiveDrones_ship(self):
        self.buildTested = 0
        attr = "maxActiveDrones"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 6
        fLvl = 4
        fIngame = 9
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
