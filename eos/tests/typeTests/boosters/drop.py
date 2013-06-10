from eos.tests import TestBase
from eos import db
from eos.types import Fit, Booster, Character, Ship, Module

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.f = Fit()
        self.c = Character("testDrop")
        self.f.character = self.c
        self.f.ship = Ship(db.getItem("Rifter"))
        self.i = db.getItem("Strong Drop Booster")
        self.i2 = db.getItem("Heavy Modulated Energy Beam I")
        self.i3 = db.getItem("Large Armor Repairer I")
        self.turret = Module(self.i2)
        self.repper = Module(self.i3)
        self.booster = Booster(self.i)
        self.f.boosters.append(self.booster)
        self.f.modules.append(self.turret)
        self.f.modules.append(self.repper)

    def test_trackingSpeed(self):
        self.f.calculateModifiedAttributes()
        original = self.i2.getAttribute("trackingSpeed")
        self.assertAlmostEquals(original * 1.375, self.turret.getModifiedItemAttr("trackingSpeed"))

    def test_falloffPenalty(self):
        self.booster.getSideEffect("boosterTurretFalloffPenalty").active = True
        self.f.calculateModifiedAttributes()
        original = self.i2.getAttribute("falloff")
        self.assertAlmostEquals(original * 0.7, self.turret.getModifiedItemAttr("falloff"))

    def test_armorRepairPenalty(self):
        self.booster.getSideEffect("boosterArmorRepairAmountPenalty").active = True
        self.f.calculateModifiedAttributes()
        original = self.i3.getAttribute("armorDamageAmount")
        self.assertAlmostEquals(original * 0.7, self.repper.getModifiedItemAttr("armorDamageAmount"))

    def test_maxVelocityPenalty(self):
        self.booster.getSideEffect("boosterMaxVelocityPenalty").active = True
        self.f.calculateModifiedAttributes()
        original = self.f.ship.item.getAttribute("maxVelocity")
        self.assertAlmostEquals(original * 0.7, self.f.ship.getModifiedItemAttr("maxVelocity"))

    def test_shieldCapacity(self):
        self.booster.getSideEffect("boosterShieldCapacityPenalty").active = True
        self.f.calculateModifiedAttributes()
        original = self.f.ship.item.getAttribute("shieldCapacity")
        self.assertAlmostEquals(original * 0.7, self.f.ship.getModifiedItemAttr("shieldCapacity"))
