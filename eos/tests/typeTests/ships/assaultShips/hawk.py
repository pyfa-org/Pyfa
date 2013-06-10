from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Hawk"

    # Caldari Frigate Skill Bonus:
    # 5% bonus to Missile Kinetic Damage per level
    # Actually it's 10%, CCP forgot to change description after boost

    def test_caldariFrigate_kineticDamage_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Thorn Rocket"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Thorn Rage Rocket"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileLight(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Bloodclaw Light Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileLightAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Bloodclaw Precision Light Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileLightFof(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Serpent F.O.F. Light Missile I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileAssault(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Terror Assault Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileAssaultAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Terror Rage Assault Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileHeavy(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Scourge Heavy Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileHeavyAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Scourge Fury Heavy Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileHeavyFof(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Hydra F.O.F. Heavy Missile I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Juggernaut Torpedo"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Juggernaut Rage Torpedo"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Wrath Cruise Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Wrath Precision Cruise Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Dragon F.O.F. Cruise Missile I"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileCitadelTorpedo(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Rift Citadel Torpedo"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileCitadelCruise(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Rajas Citadel Cruise Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeMissileLightNoSkillrqMissileOp(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Civilian Bloodclaw Light Missile"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariFrigate_kineticDamage_chargeOther(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "EMP S"
        skill = "Caldari Frigate"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Assault Frigates Skill Bonus:
    # 10% bonus to Missile Velocity per level

    def test_assaultShips_maxVelocity_chargeMissileRocket(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Foxfire Rocket"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileRocketAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Phalanx Javelin Rocket"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileLight(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Flameburst Light Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileLightAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Piranha Precision Light Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileLightFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Seeker F.O.F. Light Missile I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileAssault(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Terror Assault Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileAssaultAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Hellfire Rage Assault Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileHeavy(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Havoc Heavy Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileHeavyAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Thunderbolt Fury Heavy Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileHeavyFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Hellhound F.O.F. Heavy Missile I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Inferno Torpedo"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Bane Javelin Torpedo"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Devastator Cruise Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Paradise Precision Cruise Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Exterminator F.O.F. Light Missile I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileCitadelTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Rift Citadel Torpedo"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileCitadelCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Thunar Citadel Cruise Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileDefender(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Defender I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_maxVelocity_chargeMissileLightNoSkillrqMissileOp(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Civilian Bloodclaw Light Missile"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Assault Frigates Skill Bonus:
    # 7.5% bonus to Shield Boost Amount per level

    def test_assaultShips_shieldBonus_moduleShieldBoosterSkillrqShieldop(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Small Shield Booster I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)


    def test_assaultShips_shieldBonus_moduleShieldBoosterSkillrqCapitalShieldop(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Capital Shield Booster I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_shieldBonus_moduleShieldBoosterNoSkillrq(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Civilian Shield Booster I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_assaultShips_shieldBonus_moduleOther(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Small Shield Transporter I"
        skill = "Assault Frigates"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
