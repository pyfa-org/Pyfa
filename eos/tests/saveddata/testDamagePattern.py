from eos.tests import TestBase
from eos import db
from eos.types import Fit, DamagePattern, Ship, Module, State

class Test(TestBase):
    def test_rawEhp(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        expected = 0
        for type in ("shieldCapacity", "armorHP", "hp"):
            expected += f.ship.getModifiedItemAttr(type)

        self.assertEquals(expected, sum(f.ehp.values()))

    def test_uniformEhp(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        f.damagePattern = DamagePattern(25, 25, 25 ,25)
        self.assertAlmostEquals(3094, sum(f.ehp.values()), 0)

    def test_passiveRechargeUniform(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        f.damagePattern = DamagePattern(25, 25, 25, 25)
        self.assertAlmostEquals(3.86, f.effectiveTank["passiveShield"], 2)

    def test_armorRepairUniform(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        f.damagePattern = DamagePattern(25, 25, 25 ,25)
        m = Module(db.getItem("Small Armor Repairer I"))
        m.state = State.ACTIVE
        f.modules.append(m)
        f.calculateModifiedAttributes()
        self.assertAlmostEquals(19.3, f.effectiveTank["armorRepair"], 1)

    def test_shieldBoostUniform(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        f.damagePattern = DamagePattern(25, 25, 25 ,25)
        m = Module(db.getItem("Small Shield Booster I"))
        m.state = State.ACTIVE
        f.modules.append(m)
        f.calculateModifiedAttributes()
        self.assertAlmostEquals(26.3, f.effectiveTank["shieldRepair"],1)

    def test_hullRepairUniform(self):
        f = Fit()
        f.ship = Ship(db.getItem("Wolf"))
        f.damagePattern = DamagePattern(25, 25, 25 ,25)
        m = Module(db.getItem("Small Hull Repairer I"))
        m.state = State.ACTIVE
        f.modules.append(m)
        f.calculateModifiedAttributes()
        self.assertAlmostEquals(f.extraAttributes["hullRepair"], f.effectiveTank["hullRepair"],1)

    def test_importPattern(self):
        d = DamagePattern.importPatterns("Test = EM:5, THERM:42, KIN:1302, EXP:6")[0]
        self.assertEquals(d.name, "Test")
        self.assertEquals(d.emAmount, 5)
        self.assertEquals(d.thermalAmount, 42)
        self.assertEquals(d.kineticAmount, 1302)
        self.assertEquals(d.explosiveAmount, 6)

    def test_exportPattern(self):
        d = DamagePattern(5, 42, 1302, 6)
        d.name = "Test"
        self.assertEquals(DamagePattern.exportPatterns(d), "Test = EM:5, Therm:42, Kin:1302, Exp:6")

