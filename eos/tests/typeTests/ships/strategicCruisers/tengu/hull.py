from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Tengu"

    # Caldari Strategic Cruiser Skill Bonus:
    # 5% Reduction in the amount of heat damage absorbed by modules per level

    def test_caldariStrategicCruiser_heatDamage_moduleAfterburner(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "100MN Afterburner I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleArmorHardener(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Armor Explosive Hardener I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleArmorRepairProjector(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Small Remote Armor Repair System I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleArmorRepairer(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Medium Armor Repairer I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleCapacitorBooster(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Heavy Capacitor Booster I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleECCM(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "ECCM - Gravimetric I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleECM(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "ECM - Ion Field Projector I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleEnergyDestabilizer(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Medium Energy Neutralizer I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleEnergyTransferArray(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Small Energy Transfer Array I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleEnergyVampire(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Heavy Nosferatu I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleEnergyWeapon(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Dual Heavy Beam Laser I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleHullRepairer(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Small Hull Repairer I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleHybridWeapon(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Dual 250mm Railgun I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherAssault(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Assault Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherCitadel(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Citadel Torpedo Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherCruise(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Cruise Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherHeavy(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Heavy Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherHeavyAssault(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Heavy Assault Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherRocket(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Rocket Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherSiege(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Siege Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleMissileLauncherStandard(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Standard Missile Launcher I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleProjectileWeapon(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Dual 180mm AutoCannon I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleShieldBooster(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "X-Large Shield Booster I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleShieldHardener(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Invulnerability Field I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleShieldTransporter(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Large Shield Transporter I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleStasisWeb(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Stasis Webifier I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariStrategicCruiser_heatDamage_moduleWarpScrambler(self):
        self.buildTested = 0
        attr = "heatDamage"
        item = "Warp Disruptor I"
        skill = "Caldari Strategic Cruiser"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
