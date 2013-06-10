from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.hull = "Proteus"
        self.sub = "Proteus Defensive - Augmented Plating"
        self.skill = "Gallente Defensive Systems"

    # Subsystem Skill Bonus:
    # 10% bonus to armor hitpoints per level

    def test_gallenteDefensiveSystems_armorHP_ship(self):
        self.buildTested = 0
        attr = "armorHP"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # Add slots to ship

    def test_static_hiSlots_ship(self):
        self.buildTested = 0
        attr = "hiSlots"
        iIngame = 0.0
        fIngame = 0.0
        iEos = self.getShipAttr(attr, ship=self.hull) or 0.0
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub) or 0.0
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_medSlots_ship(self):
        self.buildTested = 0
        attr = "medSlots"
        iIngame = 0.0
        fIngame = 0.0
        iEos = self.getShipAttr(attr, ship=self.hull) or 0.0
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub) or 0.0
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_lowSlots_ship(self):
        self.buildTested = 0
        attr = "lowSlots"
        iIngame = 0.0
        fIngame = 2.0
        iEos = self.getShipAttr(attr, ship=self.hull) or 0.0
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub) or 0.0
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +1400000 kg mass

    def test_static_mass_ship(self):
        self.buildTested = 0
        attr = "mass"
        iIngame = 5341000.0
        fIngame = 6741000.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # 168 m signature radius

    def test_static_signatureRadius_ship(self):
        self.buildTested = 0
        attr = "signatureRadius"
        ingame = 168.0
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    # Hidden bonus:
    # 280 m3 cargohold capacity

    def test_static_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        ingame = 280.0
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    # Hidden bonus:
    # Assign ship armor resistances

    def test_static_armorEmDamageResonance_ship(self):
        self.buildTested = 0
        attr = "armorEmDamageResonance"
        ingame = 0.5
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_armorExplosiveDamageResonance_ship(self):
        self.buildTested = 0
        attr = "armorExplosiveDamageResonance"
        ingame = 0.9
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_armorKineticDamageResonance_ship(self):
        self.buildTested = 0
        attr = "armorKineticDamageResonance"
        ingame = 0.1625
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_armorThermalDamageResonance_ship(self):
        self.buildTested = 0
        attr = "armorThermalDamageResonance"
        ingame = 0.325
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    # Hidden bonus:
    # Assign ship shield resistances

    def test_static_shieldEmDamageResonance_ship(self):
        self.buildTested = 0
        attr = "shieldEmDamageResonance"
        ingame = 1.0
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_shieldExplosiveDamageResonance_ship(self):
        self.buildTested = 0
        attr = "shieldExplosiveDamageResonance"
        ingame = 0.5
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_shieldKineticDamageResonance_ship(self):
        self.buildTested = 0
        attr = "shieldKineticDamageResonance"
        ingame = 0.15
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    def test_static_shieldThermalDamageResonance_ship(self):
        self.buildTested = 0
        attr = "shieldThermalDamageResonance"
        ingame = 0.4
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

    # Hidden bonus:
    # +3650 armor hp

    def test_static_armorHP_ship(self):
        self.buildTested = 0
        attr = "armorHP"
        iIngame = 100.0
        fIngame = 3750.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +2400 shield capacity

    def test_static_shieldCapacity_ship(self):
        self.buildTested = 0
        attr = "shieldCapacity"
        iIngame = 100.0
        fIngame = 2500.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +1620 seconds shield recharge rate

    def test_static_shieldRechargeRate_ship(self):
        self.buildTested = 0
        attr = "shieldRechargeRate"
        iIngame = 10000.0
        fIngame = 1630000.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
