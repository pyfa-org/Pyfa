from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Freki"

    # Minmatar Frigate Skill Bonus:
    # 12.5% Small Projectile Turret damage per level

    def test_minmatarFrigate_damageMultiplier_moduleProjectileWeaponSmall(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "280mm Howitzer Artillery I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.125
        fLvl = 4
        fIngame = 1.5
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_damageMultiplier_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "damageMultiplier"
        item = "425mm AutoCannon I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Minmatar Frigate Skill Bonus:
    # 30% bonus to Stasis Webifier Range per level

    def test_minmatarFrigate_maxRange_moduleStasisWebSkillrqPropjamm(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Stasis Webifier I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_maxRange_moduleStasisWebNoSkillrq(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Civilian Stasis Webifier"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.3
        fLvl = 4
        fIngame = 2.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_minmatarFrigate_maxRange_moduleOtherSkillrqPropjamm(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Warp Disruptor I"
        skill = "Minmatar Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Special Ability:
    # 50% Small Projectile Turret optimal range bonus

    def test_static_maxRange_moduleProjectileWeaponSmall(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "250mm Light Artillery Cannon I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "650mm Artillery Cannon I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Special Ability:
    # 50% Small Projectile Turret falloff bonus

    def test_static_falloff_moduleProjectileWeaponSmall(self):
        self.buildTested = 0
        attr = "falloff"
        item = "200mm AutoCannon I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.5
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_falloff_moduleProjectileWeaponOther(self):
        self.buildTested = 0
        attr = "falloff"
        item = "Dual 180mm AutoCannon I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Special Ability:
    # 75% afterburner and microwarpdrive capacitor consumption bonus

    def test_static_capacitorNeed_moduleAfterburnerSkillrqHighSpeedManeuvering(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "1MN MicroWarpdrive I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 0.25
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleAfterburnerSkillrqAfterburner(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "1MN Afterburner I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 0.25
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleAfterburnerNoSkillrq(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "Civilian Afterburner"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 0.25
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_capacitorNeed_moduleOther(self):
        self.buildTested = 0
        attr = "capacitorNeed"
        item = "ECM Burst I"
        ship_other = "Punisher"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
