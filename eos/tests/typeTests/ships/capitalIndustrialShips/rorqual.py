from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Rorqual"

    # Capital Industrial Ships skill bonuses:
    # -5% reduction in fuel consumption for industrial cores per level

    def test_capitalIndustrialShips_consumptionQuantity_moduleSiegeModuleSkillrqIndustrialReconfiguration(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Industrial Core I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_consumptionQuantity_moduleOther(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Clone Vat Bay I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Capital Industrial Ships skill bonuses:
    # 10% bonus to effectiveness of mining foreman gang links per level when in deployed mode

    def test_capitalIndustrialShips_commandBonus_moduleGangCoordinatorSkillrqMiningDirectorSiegeActive(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Mining Foreman Link - Laser Optimization I"
        skill = "Capital Industrial Ships"
        miscitm = ("Industrial Core I", "active")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_commandBonus_moduleGangCoordinatorSkillrqMiningDirectorSiegeOnline(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Mining Foreman Link - Harvester Capacitor Efficiency I"
        skill = "Capital Industrial Ships"
        miscitm = ("Industrial Core I", "online")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_commandBonus_moduleGangCoordinatorSkillrqOtherSiegeActive(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Armored Warfare Link - Damage Control I"
        skill = "Capital Industrial Ships"
        miscitm = ("Industrial Core I", "active")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Capital Industrial Ships skill bonuses:
    # 50% bonus to the range of Capital Shield Transporters per level

    def test_capitalIndustrialShips_shieldTransferRange_moduleShieldTransporterCapital(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Capital Shield Transporter I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 1.5
        fLvl = 4
        fIngame = 3.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_shieldTransferRange_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "shieldTransferRange"
        item = "Large Shield Transporter I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Capital Industrial Ships skill bonuses:
    # 20% bonus to drone hitpoints per level

    def test_capitalIndustrialShips_hp_droneCombat(self):
        self.buildTested = 0
        item = "Bouncer I"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_hp_droneLogistic(self):
        self.buildTested = 0
        item = "Heavy Shield Maintenance Bot I"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_hp_droneEwar(self):
        self.buildTested = 0
        item = "Berserker TP-900"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_hp_droneCapDrain(self):
        self.buildTested = 0
        item = "Praetor EV-900"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_hp_droneWeb(self):
        self.buildTested = 0
        item = "Berserker SW-900"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_hp_droneMining(self):
        self.buildTested = 0
        item = "Harvester Mining Drone"
        skill = "Capital Industrial Ships"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Capital Industrial Ships skill bonuses:
    # 20% bonus to drone damage per level

    def test_capitalIndustrialShips_damageMultiplier_droneCombat(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Warrior I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 1.2
        fLvl = 4
        fIngame = 1.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_capitalIndustrialShips_damageMultiplier_other(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Heat Sink I"
        skill = "Capital Industrial Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonuses:
    # 900% bonus to the range of survey scanners

    def test_static_surveyScanRange_moduleSurveyScanner(self):
        self.buildTested = 0
        attr = "surveyScanRange"
        item = "Survey Scanner I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 10.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonuses:
    # 200% bonus to the range of cargo scanners

    def test_static_cargoScanRange_moduleCargoScanner(self):
        self.buildTested = 0
        attr = "cargoScanRange"
        item = "Cargo Scanner I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 3.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_falloff_moduleCargoScanner(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Cargo Scanner I"
        ship_other = "Rifter"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # 99% reduction in CPU need for Gang Link modules

    def test_static_cpu_moduleGangCoordinatorSkillrqLeadership(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Information Warfare Link - Recon Operation I"
        ship_other = "Abaddon"
        iIngame = 1.0
        fIngame = 0.01
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleGangCoordinatorNoSkillrqLeadership(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Command Processor I"
        ship_other = "Abaddon"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Can use 3 Gang Link modules simultaneously.

    def test_static_maxGroupActive_moduleGangCoordinator(self):
        self.buildTested = 0
        attr = "maxGroupActive"
        item = "Siege Warfare Link - Shield Efficiency I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 3.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxGroupActive_moduleOther(self):
        self.buildTested = 0
        attr = "maxGroupActive"
        item = "100MN MicroWarpdrive I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Advanced Spaceship Command Skill Bonus:
    # 5% Bonus to the agility of ship per skill level
    # Moved from Advanced Spaceship Command skill tests, not listed as bonus of ship

    def test_advancedSpaceshipCommand_agility_ship(self):
        self.buildTested = 0
        attr = "agility"
        skill = "Advanced Spaceship Command"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
