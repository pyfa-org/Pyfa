from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Falcon"

    # Caldari Cruiser Skill Bonus:
    # 5% Bonus to Medium Hybrid Damage Per Level

    def test_caldariCruiser_damageMultiplier_moduleHybridWeaponMedium(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Dual 150mm Railgun I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "75mm Gatling Rail I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Cruiser Skill Bonus:
    # 10% Bonus to ECM Target Jammer capacitor use per level

    def test_caldariCruiser_capacitorNeed_moduleECM(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "ECM - Phase Inverter I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariCruiser_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "ECM Burst I"
        skill = "Caldari Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Recon Ships Skill Bonus:
    # 30% bonus to ECM Target Jammer strength per level

    def test_reconShips_scanGravimetricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM - White Noise Generator I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanGravimetricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanGravimetricStrengthBonus"
        item = "ECM Burst I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanLadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM - Multispectral Jammer I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanLadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanLadarStrengthBonus"
        item = "ECM Burst I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanMagnetometricStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM - Ion Field Projector I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanMagnetometricStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanMagnetometricStrengthBonus"
        item = "ECM Burst I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanRadarStrengthBonus_moduleEcm(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM - Spatial Destabilizer I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_scanRadarStrengthBonus_moduleOther(self):
        self.buildTested = 0
        attr = "scanRadarStrengthBonus"
        item = "ECM Burst I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Recon Ships Skill Bonus:
    # -96% to -100% reduced CPU need for cloaking device per level
    # Static part

    def test_static_cpu_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Prototype Cloaking Device I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 0.05
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleOther(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Warp Disruptor I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Recon Ships Skill Bonus:
    # -96% to -100% reduced CPU need for cloaking device per level
    # Dynamic part

    def test_reconShips_cpu_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Prototype Cloaking Device I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 0.04
        fLvl = 4
        fIngame = 0.01
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_reconShips_cpu_moduleOther(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Warp Core Stabilizer I"
        skill = "Recon Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
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
        fItem = "Covert Cynosural Field Generator I"
        fIngame = 30000.0
        iEos = self.getItemAttr(attr, iItem, ship=self.ship)
        fEos = self.getItemAttr(attr, fItem, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 80% reduction in liquid ozone consumption for cynosural field generation

    def test_static_consumptionQuantity_moduleCynosuralField(self):
        self.buildTested = 0
        attr = "consumptionQuantity"
        item = "Cynosural Field Generator I"
        ship_other = "Buzzard"
        iIngame = 1.0
        fIngame = 0.2
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 50% reduction in cynosural field duration

    def test_static_duration_moduleCynosuralField(self):
        self.buildTested = 0
        attr = "duration"
        item = "Covert Cynosural Field Generator I"
        ship_other = "Buzzard"
        iIngame = 1.0
        fIngame = 0.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
