from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Anshar"

    # Gallente Freighter Skill Bonus:
    # 5% bonus to cargo hold capacity per level

    def test_gallenteFreighter_capacity_ship(self):
        self.buildTested = 0
        attr = "capacity"
        skill = "Gallente Freighter"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Freighter Skill Bonus:
    # 5% bonus to agility per level

    def test_gallenteFreighter_agility_ship(self):
        self.buildTested = 0
        attr = "agility"
        skill = "Gallente Freighter"
        iLvl = 1
        iIngame = 0.95
        fLvl = 4
        fIngame = 0.8
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Jump Freighters Skill Bonus:
    # 10% bonus to shield hitpoints per level

    def test_jumpFreighters_shieldCapacity_ship(self):
        self.buildTested = 0
        attr = "shieldCapacity"
        skill = "Jump Freighters"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Jump Freighters Skill Bonus:
    # 10% bonus to armor hitpoints per level

    def test_jumpFreighters_armorHp_ship(self):
        self.buildTested = 0
        attr = "armorHP"
        skill = "Jump Freighters"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Jump Freighters Skill Bonus:
    # 10% bonus to hull hitpoints per level

    def test_jumpFreighters_hp_ship(self):
        self.buildTested = 0
        attr = "hp"
        skill = "Jump Freighters"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Jump Freighters Skill Bonus:
    # 10% reduction in jump fuel need per level

    def test_jumpFreighters_jumpDriveConsumptionAmount_ship(self):
        self.buildTested = 0
        attr = "jumpDriveConsumptionAmount"
        skill = "Jump Freighters"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getShipAttr(attr, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getShipAttr(attr, skill=(skill, fLvl), ship=self.ship)
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
