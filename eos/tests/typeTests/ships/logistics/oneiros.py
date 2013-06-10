from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Oneiros"

    # Gallente Cruiser Skill Bonus:
    # 150% bonus to Remote Armor Repair System range per level

    def test_gallenteCruiser_maxRange_moduleRemoteArmorRepairer(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Large Remote Armor Repair System I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_maxRange_moduleRemoteArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Capital Remote Armor Repair System I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_maxRange_moduleRemoteArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Remote Armor Repair System"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 150% bonus to Tracking Link range per level

    def test_gallenteCruiser_maxRange_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Tracking Link I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 2.5
        fLvl = 4
        fIngame = 7.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Remote Sensor Booster I"
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
    # 20% bonus to Armor Maintenance Bot transfer amount per level
    # Actually static 100% bonus, anyway cruiser skill must be at V level

    def test_static_armorDamageAmount_droneLogistics(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Light Armor Maintenance Bot I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_armorDamageAmount_other(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Small Armor Repairer I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Logistics Skill Bonus:
    # 15% reduction in Remote Armor Repair System capacitor use per level

    def test_logistics_capacitorNeed_moduleRemoteArmorRepairer(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Medium Remote Armor Repair System I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleRemoteArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Capital Remote Armor Repair System I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleRemoteArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Remote Armor Repair System"
        skill = "Logistics"
        iLvl = 1
        iIngame = 0.85
        fLvl = 4
        fIngame = 0.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Explosion Dampening Field I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Logistics Skill Bonus:
    # 10% bonus to Tracking Link efficiency per level

    def test_logistics_maxRangeBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_maxRangeBonus_moduleOther(self):
        self.buildTested = 0
        attr = "maxRangeBonus"
        item = "Medium Hybrid Locus Coordinator I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_falloffBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_falloffBonus_moduleOther(self):
        self.buildTested = 0
        attr = "falloffBonus"
        item = "Tracking Disruptor I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_trackingSpeedBonus_moduleTrackingLink(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Link I"
        skill = "Logistics"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_logistics_trackingSpeedBonus_moduleOther(self):
        self.buildTested = 0
        attr = "trackingSpeedBonus"
        item = "Tracking Computer I"
        skill = "Logistics"
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
    # -65% power need for Remote Armor Repair Systems

    def test_static_power_moduleRemoteArmorRepairer(self):
        self.buildTested = 0
        attr = "power"
        item = "Large Remote Armor Repair System I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.35
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleRemoteArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "power"
        item = "Capital Remote Armor Repair System I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.35
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleRemoteArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "power"
        item = "Civilian Remote Armor Repair System"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 0.35
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleOther(self):
        self.buildTested = 0
        attr = "power"
        item = "Small Energy Neutralizer I"
        ship_other = "Omen"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
