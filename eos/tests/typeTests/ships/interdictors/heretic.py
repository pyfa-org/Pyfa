from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Heretic"

    # Destroyer Skill Bonus:
    # 5% bonus to rocket damage per level

    def test_destroyers_emDamage_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Gremlin Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_emDamage_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Gremlin Rage Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_emDamage_chargeMissileOther(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Torrent Assault Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_explosiveDamage_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Phalanx Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_explosiveDamage_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Phalanx Javelin Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_explosiveDamage_chargeMissileOther(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Exterminator F.O.F. Light Missile I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_kineticDamage_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Thorn Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_kineticDamage_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Thorn Javelin Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_kineticDamage_chargeMissileOther(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Bloodclaw Light Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_thermalDamage_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Foxfire Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_thermalDamage_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Foxfire Rage Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_thermalDamage_chargeMissileOther(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Inferno Torpedo"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Destroyer Skill Bonus:
    # 5% bonus to rocket explosion velocity per level

    def test_destroyers_aoeVelocity_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Foxfire Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Gremlin Rage Rocket"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Destroyer Skill Bonus:
    # 5% bonus to missile explosion velocity per level

    def test_destroyers_aoeVelocity_chargeMissileLight(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Sabretooth Light Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileLightAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Piranha Fury Light Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileLightFof(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Firefly F.O.F. Light Missile I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileLightNoSkillrqMissileOp(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Civilian Bloodclaw Light Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileAssault(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Fulmination Assault Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileAssaultAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Terror Javelin Assault Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileHeavy(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Thunderbolt Heavy Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileHeavyAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Scourge Fury Heavy Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileHeavyFof(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Eradicator F.O.F. Heavy Missile I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Juggernaut Torpedo"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Inferno Rage Torpedo"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Devastator Cruise Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Paradise Fury Cruise Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Hunter F.O.F. Cruise Missile I"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileCitadelTorpedo(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Doom Citadel Torpedo"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_destroyers_aoeVelocity_chargeMissileCitadelCruise(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Rajas Citadel Cruise Missile"
        skill = "Destroyers"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Interdictors Skill Bonus:
    # 5% bonus to missile velocity per level

    def test_interdictors_maxVelocity_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Gremlin Rocket"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Phalanx Rage Rocket"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileLight(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Flameburst Light Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileLightAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Piranha Precision Light Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileLightFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Seeker F.O.F. Light Missile I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileAssault(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Hellfire Assault Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileAssaultAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Torrent Rage Assault Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileHeavy(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Scourge Heavy Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileHeavyAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Widowmaker Fury Heavy Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileHeavyFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Hydra F.O.F. Heavy Missile I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Juggernaut Torpedo"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Bane Javelin Torpedo"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Devastator Cruise Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Wrath Precision Cruise Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Dragon F.O.F. Cruise Missile I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileCitadelTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Doom Citadel Torpedo"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileCitadelCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Thunar Citadel Cruise Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileDefender(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Defender I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_maxVelocity_chargeMissileLightNoSkillrqMissileOp(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Civilian Bloodclaw Light Missile"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Interdictors Skill Bonus:
    # 10% bonus to Interdiction Sphere Launcher rate of fire per level

    def test_interdictors_speed_moduleLauncherInterdictionSphere(self):
        self.buildTested = 0
        attr = "speed"
        item = "Interdiction Sphere Launcher I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_speed_moduleOther(self):
        self.buildTested = 0
        attr = "speed"
        item = "Rocket Launcher I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_moduleReactivationDelay_moduleLauncherInterdictionSphere(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        item = "Interdiction Sphere Launcher I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 0.9
        fLvl = 4
        fIngame = 0.6
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_interdictors_moduleReactivationDelay_moduleOther(self):
        self.buildTested = 0
        attr = "moduleReactivationDelay"
        item = "Prototype Cloaking Device I"
        skill = "Interdictors"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
