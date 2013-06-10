from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Vexor Navy Issue"

    # Gallente Cruiser Skill Bonus:
    # 5% bonus to Medium Hybrid Turret damage per skill level

    def test_gallenteCruiser_damageMultiplier_moduleHybridWeaponMedium(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "200mm Railgun I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_damageMultiplier_moduleHybridWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "75mm Gatling Rail I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to drone hitpoints per skill level

    def test_gallenteCruiser_hp_droneCombat(self):
        self.buildTested = 0
        item = "Praetor I"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_hp_droneLogistic(self):
        self.buildTested = 0
        item = "Medium Shield Maintenance Bot I"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_hp_droneEwar(self):
        self.buildTested = 0
        item = "Hobgoblin SD-300"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_hp_droneCapDrain(self):
        self.buildTested = 0
        item = "Acolyte EV-300"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_hp_droneWeb(self):
        self.buildTested = 0
        item = "Berserker SW-900"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_hp_droneMining(self):
        self.buildTested = 0
        item = "Mining Drone I"
        skill = "Gallente Cruiser"
        layers = ("shieldCapacity", "armorHP", "hp")
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = 0
        fEos = 0
        for layer in layers:
            iEos += self.getItemAttr(layer, item, skill=(skill, iLvl), ship=self.ship)
            fEos += self.getItemAttr(layer, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to drone damage per skill level

    def test_gallenteCruiser_damageMultiplier_droneCombat(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Infiltrator I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_damageMultiplier_other(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "Small Hybrid Collision Accelerator I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Gallente Cruiser Skill Bonus:
    # 10% bonus to drone mining yield per skill level

    def test_gallenteCruiser_miningAmount_droneMining(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Harvester Mining Drone"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_gallenteCruiser_miningAmount_other(self):
        self.buildTested = 0
        attr = "miningAmount"
        item = "Miner I"
        skill = "Gallente Cruiser"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
