from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Redeemer"

    # Amarr Battleship Skill Bonus:
    # 10% reduction in large energy turret capacitor use per level

    def test_amarrBattleship_capacitorNeed_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual Heavy Pulse Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrBattleship_capacitorNeed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Dual Light Pulse Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Amarr Battleship Skill Bonus:
    # 5% bonus to large energy turret rate of fire per level

    def test_amarrBattleship_speed_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "speed"
        item = "Mega Beam Laser I"
        skill = "Amarr Battleship"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_amarrBattleship_speed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Medium Beam Laser I"
        skill = "Amarr Battleship"
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
    # 7.5% bonus to large energy turret tracking per level

    def test_blackOps_trackingSpeed_moduleEnergyWeaponLarge(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Dual Heavy Pulse Laser I"
        skill = "Black Ops"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_blackOps_trackingSpeed_moduleEnergyWeaponOther(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Medium Pulse Laser I"
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
