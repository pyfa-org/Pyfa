from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Sentinel"

    # Amarr Frigate Skill Bonus:
    # 20% bonus to energy vampire transfer amount per level

    def test_amarrFrigate_powerTransferAmount_moduleEnergyVampire(self):
        self.buildTested = 0
        attr = "powerTransferAmount"
        item = "Small Nosferatu I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_powerTransferAmount_moduleOther(self):
        self.buildTested = 0
        attr = "powerTransferAmount"
        item = "Small Energy Transfer Array I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Frigate Skill Bonus:
    # 20% bonus to energy neutralizer transfer amount per level

    def test_amarrFrigate_energyDestabilizationAmount_moduleEnergyDestabilizer(self):
        self.buildTested = 0
        attr = "energyDestabilizationAmount"
        item = "Small Energy Neutralizer I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_energyDestabilizationAmount_other(self):
        self.buildTested = 0
        attr = "energyDestabilizationAmount"
        item = "Infiltrator EV-600"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Frigate Skill Bonus:
    # 5% bonus to effectiveness of tracking disruptors per level

    def test_amarrFrigate_maxRangeBonus_moduleTrackingDisruptor(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Disruptor I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_maxRangeBonus_moduleOther(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Link I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_falloffBonus_moduleTrackingDisruptor(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Disruptor I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_falloffBonus_moduleOther(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Computer I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_trackingSpeedBonus_moduleTrackingDisruptor(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Disruptor I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_trackingSpeedBonus_moduleOther(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Enhancer I"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Electronic Attack Ships Skill Bonus:
    # 40% bonus to energy vampire range per level

    def test_electronicAttackShips_powerTransferRange_moduleEnergyVampire(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Small Nosferatu I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.4
        fLvl = 4
        fIngame = 2.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_powerTransferRange_moduleOther(self):
        self.buildTested = 0
        attr = "powerTransferRange"
        item = "Small Energy Transfer Array I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Electronic Attack Ships Skill Bonus:
    # 40% bonus to energy neutralizer range per level

    def test_electronicAttackShips_energyDestabilizationRange_moduleEnergyDestabilizer(self):
        self.buildTested = 0
        attr = "energyDestabilizationRange"
        item = "Small Energy Neutralizer I"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.4
        fLvl = 4
        fIngame = 2.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_electronicAttackShips_energyDestabilizationRange_moduleOther(self):
        self.buildTested = 0
        attr = "energyDestabilizationRange"
        item = "Infiltrator EV-600"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Electronic Attack Ships Skill Bonus:
    # 5% reduction in capacitor recharge time per level

    def test_electronicAttackShips_rechargeRate_ship(self):
        self.buildTested = 0
        attr = "rechargeRate"
        skill = "Electronic Attack Ships"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
