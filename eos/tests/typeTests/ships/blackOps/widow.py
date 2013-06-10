from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Widow"

    # Caldari Battleship Skill Bonus:
    # 5% bonus to siege missile launcher rate of fire per level

    def test_caldariBattleship_speed_moduleLauncherMissileSiege(self):
        self.buildTested = 0
        attr = "speed"
        item = "Siege Missile Launcher I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 5% bonus to cruise missile launcher rate of fire per level

    def test_caldariBattleship_speed_moduleLauncherMissileCruise(self):
        self.buildTested = 0
        attr = "speed"
        item = "Cruise Missile Launcher I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_speed_moduleLauncherMissileOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Rocket Launcher I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 10% bonus to torpedo velocity per level

    def test_caldariBattleship_maxVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Inferno Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Juggernaut Javelin Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 10% bonus to cruise missile velocity per level

    def test_caldariBattleship_maxVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Wrath Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Wrath Fury Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Dragon F.O.F. Cruise Missile I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileOther(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Sabretooth Light Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Black Ops Skill Bonus:
    # 30% bonus to ECM target jammer strength per level

    def test_blackOps_scanGravimetricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM - Spatial Destabilizer I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanGravimetricStrengthBonus_moduleEcmBurst(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM Burst I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanGravimetricStrengthBonus_other(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "Vespa EC-600"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanLadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM - Phase Inverter I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanLadarStrengthBonus_moduleEcmBurst(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM Burst I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanLadarStrengthBonus_other(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "Vespa EC-600"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanMagnetometricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM - Multispectral Jammer I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanMagnetometricStrengthBonus_moduleEcmBurst(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM Burst I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanMagnetometricStrengthBonus_other(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "Vespa EC-600"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanRadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM - Ion Field Projector I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanRadarStrengthBonus_moduleEcmBurst(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM Burst I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_scanRadarStrengthBonus_other(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "Vespa EC-600"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Black Ops Skill Bonus:
    # Multiplies the cloaked velocity by 125% per level

    def test_blackOps_maxVelocity_shipCloakActive(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Black Ops"
        miscitm = ("Prototype Cloaking Device I", "active")
        iLvl = 1
        iIngame = 1.25
        fLvl = 4
        fIngame = 5.0
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_maxVelocity_shipCloakOnline(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Black Ops"
        miscitm = ("Prototype Cloaking Device I", "online")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Hidden bonus:
    # 5 seconds cloak reactivation delay

    def test_static_moduleReactivationDelay_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        item = "Prototype Cloaking Device I"
        ingame = 5000.0
        eos = self.getItemAttr(attr, item, ship=self.ship)
        self.assertAlmostEquals(eos, ingame)

    def test_static_moduleReactivationDelay_moduleOther(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        iItem = "Prototype Cloaking Device I"
        iIngame = 5000.0
        fItem = "Cynosural Field Generator I"
        fIngame = 30000.0
        iEos = self.getItemAttr(attr, iItem, ship=self.ship)
        fEos = self.getItemAttr(attr, fItem, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Note:
    # No targeting delay after decloaking

    def test_static_cloakingTargetingDelay_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cloakingTargetingDelay"
        item = "Prototype Cloaking Device I"
        ingame = 0.0
        eos = self.getItemAttr(attr, item, ship=self.ship)
        self.assertAlmostEquals(eos, ingame)
