from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Ragnarok"

    # Minmatar Titan Skill Bonuses:
    # 125% bonus to Capital Projectile Turret damage per level

    def test_minmatarTitan_damageMultiplier_moduleProjectileWeaponCapital(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Quad 3500mm Siege Artillery I"
        skill = "Minmatar Titan"
        iLvl = 1
        iIngame = 2.25
        fLvl = 4
        fIngame = 6.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarTitan_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "650mm Artillery Cannon I"
        skill = "Minmatar Titan"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Titan Skill Bonuses:
    # 7.5% reduction in gang members' signature radius per level

    def test_minmatarTitan_signatureRadius_fleetShip(self):
        self.buildTested = 0
        attr = "signatureRadius"
        skill = "Minmatar Titan"
        iLvl = 1
        iIngame = 0.925
        fLvl = 4
        fIngame = 0.7
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship, gang=True)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship, gang=True)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Titan Skill Bonuses:
    # Can fit 1 additional Warfare Link module per level

    def test_minmatarTitan_maxGroupActive_moduleGangCoordinator(self):
        self.buildTested = 0
        attr = "maxGroupActive"
        skill = "Minmatar Titan"
        item = "Skirmish Warfare Link - Evasive Maneuvers I"
        iLvl = 1
        iIngame = 2
        fLvl = 4
        fIngame = 5
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarTitan_maxGroupActive_moduleOther(self):
        self.buildTested = 0
        attr = "maxGroupActive"
        skill = "Minmatar Titan"
        item = "ECM Burst I"
        iLvl = 1
        iIngame = 1
        fLvl = 4
        fIngame = 1
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame - iIngame
        dEos = fEos - iEos
        self.assertAlmostEquals(dEos, dIngame)

    # 99% reduction in CPU need for Warfare Link modules

    def test_static_cpu_moduleGangCoordinatorSkillrqLeadership(self):
        self.buildTested = 0
        attr = "cpu"
        item = "Information Warfare Link - Sensor Integrity I"
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
