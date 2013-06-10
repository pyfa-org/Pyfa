from eos.tests import TestBase

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.ship = "Golem"

    # Caldari Battleship Skill Bonus:
    # 10% bonus to torpedo velocity per level

    def test_caldariBattleship_maxVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Juggernaut Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Juggernaut Javelin Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 10% bonus to cruise missile velocity per level

    def test_caldariBattleship_maxVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Cataclysm Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Devastator Fury Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Obliterator F.O.F. Cruise Missile I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.1
        fLvl = 4
        fIngame = 1.4
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_maxVelocity_chargeMissileOther(self):
        self.buildTested = 0
        attr = "maxVelocity"
        item = "Torrent Assault Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 5% bonus to torpedo explosion velocity per level

    def test_caldariBattleship_aoeVelocity_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Inferno Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_aoeVelocity_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Bane Rage Torpedo"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Caldari Battleship Skill Bonus:
    # 5% bonus to cruise missile explosion velocity per level

    def test_caldariBattleship_aoeVelocity_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Wrath Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_aoeVelocity_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Paradise Fury Cruise Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_aoeVelocity_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Dragon F.O.F. Cruise Missile I"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.05
        fLvl = 4
        fIngame = 1.2
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_caldariBattleship_aoeVelocity_chargeMissileOther(self):
        self.buildTested = 0
        attr = "aoeVelocity"
        item = "Thunderbolt Heavy Missile"
        skill = "Caldari Battleship"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Marauders Skill Bonus:
    # 7.5% bonus to shield boost amount per level

    def test_marauders_shieldBonus_moduleShieldBooster(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Small Shield Booster I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_marauders_shieldBonus_moduleShieldBoosterCapital(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Capital Shield Booster I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_marauders_shieldBonus_moduleShieldBoosterCivilian(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Civilian Shield Booster I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_marauders_shieldBonus_moduleOther(self):
        self.buildTested = 0
        attr = "shieldBonus"
        item = "Large Shield Transporter I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Marauders Skill Bonus:
    # 7.5% bonus to effectiveness of target painters per level

    def test_marauders_signatureRadiusBonus_moduleTargetPainter(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Target Painter I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.075
        fLvl = 4
        fIngame = 1.3
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_marauders_signatureRadiusBonus_moduleOther(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "100MN MicroWarpdrive I"
        skill = "Marauders"
        iLvl = 1
        iIngame = 1.0
        fLvl = 4
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, skill=(skill, iLvl), ship=self.ship)
        fEos = self.getItemAttr(attr, item, skill=(skill, fLvl), ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_marauders_signatureRadiusBonus_other(self):
        self.buildTested = 0
        attr = "signatureRadiusBonus"
        item = "Warrior TP-300"
        skill = "Marauders"
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
    # 100% bonus to cruise missile and torpedo damage

    def test_static_emDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Mjolnir Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_emDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Mjolnir Javelin Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_emDamage_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Paradise Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_emDamage_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Paradise Fury Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_emDamage_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Hunter F.O.F. Cruise Missile I"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_emDamage_chargeOther(self):
        self.buildTested = 0
        attr = "emDamage"
        item = "Torrent Assault Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Bane Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Bane Rage Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Devastator Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Devastator Fury Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Obliterator F.O.F. Cruise Missile I"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_explosiveDamage_chargeOther(self):
        self.buildTested = 0
        attr = "explosiveDamage"
        item = "Havoc Heavy Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Juggernaut Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Juggernaut Rage Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Wrath Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Wrath Precision Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Dragon F.O.F. Cruise Missile I"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_kineticDamage_chargeOther(self):
        self.buildTested = 0
        attr = "kineticDamage"
        item = "Hydra F.O.F. Heavy Missile I"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeMissileTorpedo(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Inferno Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeMissileTorpedoAdvanced(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Inferno Javelin Torpedo"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeMissileCruise(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Cataclysm Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeMissileCruiseAdvanced(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Cataclysm Fury Cruise Missile"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeMissileCruiseFof(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Phoenix F.O.F. Cruise Missile I"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_thermalDamage_chargeOther(self):
        self.buildTested = 0
        attr = "thermalDamage"
        item = "Foxfire Rocket"
        ship_other = "Scorpion"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 100% bonus to range of tractor beams

    def test_static_maxRange_moduleTractorBeam(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "Small Tractor Beam I"
        ship_other = "Megathron"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    def test_static_maxRange_moduleOther(self):
        self.buildTested = 0
        attr = "maxRange"
        item = "ECCM Projector I"
        ship_other = "Megathron"
        iIngame = 1.0
        fIngame = 1.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)

    # Role Bonus:
    # 100% bonus to velocity of tractor beams

    def test_static_maxTractorVelocity_moduleTractorBeam(self):
        self.buildTested = 0
        attr = "maxTractorVelocity"
        item = "Small Tractor Beam I"
        ship_other = "Megathron"
        iIngame = 1.0
        fIngame = 2.0
        iEos = self.getItemAttr(attr, item, ship=ship_other)
        fEos = self.getItemAttr(attr, item, ship=self.ship)
        dIngame = fIngame / iIngame
        dEos = fEos / iEos
        self.assertAlmostEquals(dEos, dIngame)
