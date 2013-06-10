from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.hull = "Tengu"
        self.sub = "Tengu Propulsion - Interdiction Nullifier"
        self.skill = "Caldari Propulsion Systems"

    # Subsystem Skill Bonus:
    # 5% increased agility per level

    def test_caldariPropulsionSystems_agility_ship(self):
        self.buildTested = 0
        attr = "agility"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getShipAttr(attr, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # Immunity to non-targeted interdiction

    def test_static_warpBubbleImmune_ship(self):
        self.buildTested = 0
        attr = "warpBubbleImmune"
        ingame = 1.0
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)

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
        fIngame = 0.0
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
        iIngame = 8201000.0
        fIngame = 9601000.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +155 m/s speed

    def test_static_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        iIngame = 10.0
        fIngame = 165.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # Set inertia modifier to 0.559

    def test_static_agility_ship(self):
        self.buildTested = 0
        attr = "agility"
        ingame = 0.559
        eos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        self.assertAlmostEquals(eos, ingame)
