from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Augoror"

    # Amarr Cruiser Skill Bonus:
    # 10% bonus to armor hitpoints per level

    def test_amarrCruiser_armorHP_ship(self):
        self.buildTested = 0
        attr = "armorHP"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Cruiser Skill Bonus:
    # 10% bonus to capacitor need of energy transfer arrays per level

    def test_amarrCruiser_capacitorNeed_moduleEnergyTransfer(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Energy Transfer Array I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrCruiser_capacitorNeed_moduleEnergyTransferCapital(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Capital Energy Transfer Array I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrCruiser_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Energy Neutralizer I"
        skill = "Amarr Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role bonus:
    # 500% bonus to range of energy transfer arrays

    def test_static_powerTransferRange_moduleEnergyTransfer(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Small Energy Transfer Array I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_powerTransferRange_moduleEnergyTransferCapital(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Capital Energy Transfer Array I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_powerTransferRange_moduleOther(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Medium Nosferatu I"
        ship_other = "Rupture"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
