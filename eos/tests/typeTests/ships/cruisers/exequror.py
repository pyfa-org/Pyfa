from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Exequror"

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to Cargo Capacity per level

    def test_gallenteCruiser_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to capacitor need of remote armor repair system per level

    def test_gallenteCruiser_capacitorNeed_moduleRemoteArmorRepairer(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Remote Armor Repair System I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_capacitorNeed_moduleRemoteArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Capital Remote Armor Repair System I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_capacitorNeed_moduleRemoteArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Remote Armor Repair System"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Warp Scrambler I"
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

    # Role Bonus:
    # 500% bonus to range of remote armor repair systems

    def test_static_maxRange_moduleRemoteArmorRepairer(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Large Remote Armor Repair System I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleRemoteArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Capital Remote Armor Repair System I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleRemoteArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Remote Armor Repair System"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "200mm AutoCannon I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_other(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Medium Armor Maintenance Bot I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
