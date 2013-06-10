from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Purifier"

    # Amarr Frigate Skill Bonus:
    # 10% bonus to torpedo explosion velocity per level

    def test_amarrFrigate_aoeVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Juggernaut Torpedo"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_aoeVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Bane Rage Torpedo"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_aoeVelocity_chargeMissileOther(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Gremlin Rocket"
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
    # 10% bonus to torpedo flight time per level

    def test_amarrFrigate_explosionDelay_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "explosionDelay"
        item = "Bane Torpedo"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_explosionDelay_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "explosionDelay"
        item = "Mjolnir Javelin Torpedo"
        skill = "Amarr Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrFrigate_explosionDelay_chargeMissileOther(self):
        self.buildTested = 0
        attr = "explosionDelay"
        item = "Foxfire Rocket"
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
    # 20% bonus to torpedo velocity per level

    def test_amarrFrigate_maxVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Mjolnir Torpedo"
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

    def test_amarrFrigate_maxVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Inferno Javelin Torpedo"
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

    def test_amarrFrigate_maxVelocity_chargeMissileOther(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Havoc Heavy Missile"
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

    # Covert Ops Skill Bonus:
    # 5% bonus to bomb EM damage per level

    def test_covertOps_emDamage_chargeBomb(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Electron Bomb"
        skill = "Covert Ops"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_covertOps_emDamage_chargeBombEcm(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Lockbreaker Bomb"
        skill = "Covert Ops"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_covertOps_emDamage_chargeBombEnergy(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Void Bomb"
        skill = "Covert Ops"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Covert Ops Skill Bonus:
    # 15% bonus to Torpedo EM damage per level

    def test_covertOps_emDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Mjolnir Torpedo"
        skill = "Covert Ops"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_covertOps_emDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Mjolnir Rage Torpedo"
        skill = "Covert Ops"
        iLvl = 1
        iIngame = 1.15
        fLvl = 4
        fIngame = 1.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_covertOps_emDamage_chargeOther(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Seeker F.O.F. Light Missile I"
        skill = "Covert Ops"
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
    # -99.65% reduction in Siege Missile Launcher powergrid needs

    def test_static_power_moduleLauncherMissileSiege(self):
        self.buildTested = 0
        attr = "power"
        item = "Siege Missile Launcher I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 0.0035
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_power_moduleLauncherMissileOther(self):
        self.buildTested = 0
        attr = "power"
        item = "Rocket Launcher I"
        ship_other = "Raven"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # -99.5% reduction in Cloak CPU Use

    def test_static_cpu_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Prototype Cloaking Device I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 0.005
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_cpu_moduleOther(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Damage Control I"
        ship_other = "Drake"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # -100% targeting delay after decloaking

    def test_static_cloakingTargetingDelay_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "cloakingTargetingDelay"
        item = "Prototype Cloaking Device I"
        ingame = 0.0
        eos = self.getItemAttr(attr, item, ship=self.ship)
        self.assertAlmostEquals(eos, ingame)

    # Hidden bonus:
    # 15 seconds cloak reactivation delay

    def test_static_moduleReactivationDelay_moduleCloakingDevice(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        item = "Prototype Cloaking Device I"
        ingame = 15000.0
        eos = self.getItemAttr(attr, item, ship=self.ship)
        self.assertAlmostEquals(eos, ingame)

    def test_static_moduleReactivationDelay_moduleOther(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        iItem = "Prototype Cloaking Device I"
        iIngame = 15000.0
        fItem = "Covert Cynosural Field Generator I"
        fIngame = 30000.0
        iEos = self.getItemAttr(attr, iItem, ship=self.ship)
        fEos = self.getItemAttr(attr, fItem, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
