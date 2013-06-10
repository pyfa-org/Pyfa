from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.hull = "Legion"
        self.sub = "Legion Offensive - Drone Synthesis Projector"
        self.skill = "Amarr Offensive Systems"

    # Subsystem Skill Bonus:
    # 10% bonus to medium energy turret capacitor use per level

    def test_amarrOffensiveSystems_capacitorNeed_moduleEnergyWeaponMedium(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Heavy Beam Laser I"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_capacitorNeed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual Light Beam Laser I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Subsystem Skill Bonus:
    # 10% bonus to drone damage per level

    def test_amarrOffensiveSystems_damageMultiplier_droneCombat(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Hobgoblin I"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_damageMultiplier_other(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Dual Light Pulse Laser I"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
        fEos = self.getItemAttr(attr, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Subsystem Skill Bonus:
    # 7.5% bonus to drone hitpoints per level

    def test_amarrOffensiveSystems_hp_droneCombat(self):
        self.buildTested = 0
        item = "Hammerhead I"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_hp_droneLogistic(self):
        self.buildTested = 0
        item = "Heavy Shield Maintenance Bot I"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_hp_droneEwar(self):
        self.buildTested = 0
        item = "Hammerhead SD-600"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_hp_droneCapDrain(self):
        self.buildTested = 0
        item = "Acolyte EV-300"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_hp_droneWeb(self):
        self.buildTested = 0
        item = "Berserker SW-900"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrOffensiveSystems_hp_droneNoSkillrqDrones(self):
        self.buildTested = 0
        item = "Harvester Mining Drone"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(self.skill, iLvl), ship=self.hull, miscitms=self.sub)
            fEos += self.getItemAttr(layer, item, skill=(self.skill, fLvl), ship=self.hull, miscitms=self.sub)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # Add slots to ship

    def test_static_hiSlots_ship(self):
        self.buildTested = 0
        attr = "hiSlots"
        iIngame = 0.0
        fIngame = 5.0
        iEos = self.getShipAttr(attr, ship=self.hull) or 0.0
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub) or 0.0
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_medSlots_ship(self):
        self.buildTested = 0
        attr = "medSlots"
        iIngame = 0.0
        fIngame = 1.0
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
    # Add weapon hardpoints

    def test_static_turretSlotsLeft_ship(self):
        self.buildTested = 0
        attr = "turretSlotsLeft"
        iIngame = 0.0
        fIngame = 3.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_launcherSlotsLeft_ship(self):
        self.buildTested = 0
        attr = "launcherSlotsLeft"
        iIngame = 0.0
        fIngame = 0.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +200 m3 dronebay

    def test_static_droneCapacity_ship(self):
        self.buildTested = 0
        attr = "droneCapacity"
        iIngame = 0.0
        fIngame = 200.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +50 MBit/s drone bandwidth

    def test_static_droneBandwidth_ship(self):
        self.buildTested = 0
        attr = "droneBandwidth"
        iIngame = 0.0
        fIngame = 50.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # +800000 kg mass

    def test_static_mass_ship(self):
        self.buildTested = 0
        attr = "mass"
        iIngame = 6815000.0
        fIngame = 7615000.0
        iEos = self.getShipAttr(attr, ship=self.hull)
        fEos = self.getShipAttr(attr, ship=self.hull, miscitms=self.sub)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
