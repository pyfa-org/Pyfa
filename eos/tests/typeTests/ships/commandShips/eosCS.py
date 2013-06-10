from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Eos"

    # Battlecruiser Skill Bonus:
    # 5% bonus to Medium Hybrid Turret damage per level

    def test_battlecruisers_damageMultiplier_moduleHybridWeaponMedium(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Heavy Ion Blaster I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "425mm Railgun I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Battlecruiser Skill Bonus:
    # 7.5% bonus to Armor Repairer effectiveness per level

    def test_battlecruisers_armorDamageAmount_moduleArmorRepairer(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Large Armor Repairer I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_armorDamageAmount_moduleArmorRepairerCapital(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Capital Armor Repairer I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_armorDamageAmount_moduleArmorRepairerCivilian(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Civilian Armor Repairer"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_armorDamageAmount_moduleOther(self):
        self.buildTested = 0
        attr = "armorDamageAmount"
        item = "Large Remote Armor Repair System I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Command Ships Skill Bonus:
    # +15 m3 extra Drone Bay space per level

    def test_commandShips_droneCapacity_ship(self):
        self.buildTested = 0
        attr = "droneCapacity"
        skill = "Command Ships"
        iLvl = 1
        iIngame = 15.0
        fLvl = 4
        fIngame = 60.0
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Command Ships Skill Bonus:
    # 3% bonus to effectiveness of Information Warfare Links per level

    def test_commandShips_commandBonus_moduleGangCoordinatorSkillrqInformation(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Information Warfare Link - Recon Operation I"
        skill = "Command Ships"
        iLvl = 1
        iIngame = 1.03
        fLvl = 4
        fIngame = 1.12
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_commandShips_commandBonus_moduleGangCoordinatorSkillrqOther(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Armored Warfare Link - Passive Defense I"
        skill = "Command Ships"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_commandShips_commandBonusHidden_moduleGangCoordinatorSkillrqInformation(self):
        self.buildTested = 0
        attr = "commandBonusHidden"
        item = "Information Warfare Link - Electronic Superiority I"
        skill = "Command Ships"
        iLvl = 1
        iIngame = 1.03
        fLvl = 4
        fIngame = 1.12
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 99% reduction in Warfare Link module CPU need

    def test_static_cpu_moduleGangCoordinatorSkillrqLeadership(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Siege Warfare Link - Shield Harmonizing I"
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

    # Role Bonus:
    # Can use 3 Warfare Link modules simultaneously

    def test_static_maxGroupActive_moduleGangCoordinator(self):
        self.buildTested = 0
        attr = "maxGroupActive"
        item = "Information Warfare Link - Electronic Superiority I"
        ship_other = "Brutix"
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
        item = "Internal Force Field Array I"
        ship_other = "Brutix"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
