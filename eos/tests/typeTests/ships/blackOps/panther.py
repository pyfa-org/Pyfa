from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Panther"

    # Minmatar Battleship Skill Bonus:
    # 5% bonus to large projectile turret rate of fire per level

    def test_minmatarBattleship_speed_moduleProjectileWeaponLarge(self):
        self.buildTested = 0
        attr = "speed"
        item = "Dual 650mm Repeating Artillery I"
        skill = "Minmatar Battleship"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarBattleship_speed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "425mm AutoCannon I"
        skill = "Minmatar Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Battleship Skill Bonus:
    # 5% bonus to large projectile turret damage per level

    def test_minmatarBattleship_damageMultiplier_moduleProjectileWeaponLarge(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "1400mm Howitzer Artillery I"
        skill = "Minmatar Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarBattleship_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "720mm Howitzer Artillery I"
        skill = "Minmatar Battleship"
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
    # 5% bonus to velocity per level

    def test_blackOps_maxVelocity_ship(self):
        self.buildTested = 0
        attr = "maxVelocity"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
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
        iEosNoCloak = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        iEosCloak = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEosNoCloak = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        fEosCloak = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        # Also consider speed factor w/o cloak as other effect affects speed
        dEos = (iEosNoCloak / fEosNoCloak) * (fEosCloak / iEosCloak)
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
        iEosNoCloak = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        iEosCloak = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship, miscitms=miscitm)
        fEosNoCloak = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        fEosCloak = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship, miscitms=miscitm)
        dIngame = fIngame / iIngame
        # Also consider speed factor w/o cloak as other effect affects speed
        dEos = (iEosNoCloak / fEosNoCloak) * (fEosCloak / iEosCloak)
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
