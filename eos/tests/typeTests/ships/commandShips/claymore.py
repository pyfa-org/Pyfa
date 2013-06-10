from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Claymore"

    # Battlecruiser Skill Bonus:
    # 5% bonus to Medium Projectile Turret rate of fire per level

    def test_battlecruisers_speed_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "speed"
        item = "220mm Vulcan AutoCannon I"
        skill = "Battlecruisers"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_battlecruisers_speed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "280mm Howitzer Artillery I"
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
    # 7.5% bonus to Shield Booster effectiveness per level

    def test_battlecruisers_shieldBonus_moduleShieldBooster(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Small Shield Booster I"
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

    def test_battlecruisers_shieldBonus_moduleShieldBoosterCapital(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Capital Shield Booster I"
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

    def test_battlecruisers_shieldBonus_moduleShieldBoosterCivilian(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Civilian Shield Booster I"
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

    def test_battlecruisers_shieldBonus_moduleOther(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Small Shield Transporter I"
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
    # 7.5% bonus to Medium Projectile Turret tracking speed per level

    def test_commandShips_trackingSpeed_moduleProjectileWeaponMedium(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Dual 180mm AutoCannon I"
        skill = "Command Ships"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_commandShips_trackingSpeed_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "trackingSpeed"
        item = "Dual 650mm Repeating Artillery I"
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

    # Command Ships Skill Bonus:
    # 3% bonus to effectiveness of Skirmish Warfare Links per level

    def test_commandShips_commandBonus_moduleGangCoordinatorSkillrqArmored(self):
        self.buildTested = 0
        attr = "commandBonus"
        item = "Skirmish Warfare Link - Interdiction Maneuvers I"
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
        item = "Information Warfare Link - Recon Operation I"
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

    # Role Bonus:
    # 99% reduction in Warfare Link module CPU need

    def test_static_cpu_moduleGangCoordinatorSkillrqLeadership(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Siege Warfare Link - Shield Efficiency I"
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
        item = "Skirmish Warfare Link - Evasive Maneuvers I"
        ship_other = "Prophecy"
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
        item = "ECM Burst I"
        ship_other = "Prophecy"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)
