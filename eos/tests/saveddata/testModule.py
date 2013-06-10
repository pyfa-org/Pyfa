from eos.tests import TestBase
from eos.types import Module, Fit, User, State, Ship, Slot, Hardpoint
from eos import db
import eos.db.saveddata.queries
import sqlalchemy.orm
from copy import deepcopy

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.i = db.getItem("Heat Sink I")
        self.m = Module(self.i)

    def test_clear(self):
        m = Module(db.getItem("125mm Gatling AutoCannon I"))
        m.charge = db.getItem("Phased Plasma S")
        orig = m.getModifiedItemAttr("trackingSpeed")
        chargeOrig = m.getModifiedChargeAttr("explosiveDamage")
        m.itemModifiedAttributes["trackingSpeed"] = 5
        m.chargeModifiedAttributes["explosiveDamage"] = 10
        m.clear()
        self.assertEquals(m.getModifiedItemAttr("trackingSpeed"), orig)
        self.assertEquals(m.getModifiedChargeAttr("explosiveDamage"), chargeOrig)

    def test_setItem(self):
        self.assertEquals(self.m.itemID, self.i.ID)

    def test_setPassiveActive(self):
        self.assertFalse(self.m.isValidState(State.ACTIVE))

    def test_setPassiveOverload(self):
        self.assertFalse(self.m.isValidState(State.OVERHEATED))

    def test_setActiveOverloadWhenGood(self):
        m = Module(db.getItem("Heavy Modulated Energy Beam I"))
        m.state = State.ACTIVE
        m.state = State.OVERHEATED

    def test_setWrongAmmoType(self):
        m = Module(db.getItem("125mm Gatling AutoCannon I"))
        self.assertFalse(m.isValidCharge(db.getItem("Gamma L")))

    def test_setWrongAmmoSize(self):
        m = Module(db.getItem("Dual Light Pulse Laser I"))
        self.assertFalse(m.isValidCharge(db.getItem("Gamma M")))

    def test_setWrongAmmoSubGroup(self):
        m = Module(db.getItem("Dual Light Pulse Laser I"))
        self.assertFalse(m.isValidCharge(db.getItem("Scorch S")))

    def test_setCorrectAmmo(self):
        i = db.getItem("Dual Light Pulse Laser I")
        m = Module(i)
        a = db.getItem("Gamma S")
        self.assertTrue(m.isValidCharge(a))
        m.charge = a
        self.assertEquals(m.numCharges, 1)
        self.assertEquals(m.itemID, i.ID)
        self.assertEquals(m.chargeID, a.ID)

    def test_slotRig(self):
        m = Module(db.getItem("Large Capacitor Control Circuit I"))
        self.assertEquals(Slot.RIG, m.slot)

    def test_slotSubsystem(self):
        m = Module(db.getItem("Tengu Offensive - Magnetic Infusion Basin"))
        self.assertEquals(Slot.SUBSYSTEM, m.slot)

    def test_slotHigh(self):
        m = Module(db.getItem("Salvager I"))
        self.assertEquals(Slot.HIGH, m.slot)

    def test_slotMed(self):
        m = Module(db.getItem("Cap Recharger I"))
        self.assertEquals(Slot.MED, m.slot)

    def test_slotLow(self):
        m = Module(db.getItem("Heat Sink I"))
        self.assertEquals(Slot.LOW, m.slot)

    def test_hardpointTurret(self):
        m = Module(db.getItem("Dual Light Pulse Laser I"))
        self.assertEquals(m.hardpoint, Hardpoint.TURRET)

    def test_hardpointMissile(self):
        m = Module(db.getItem("Standard Missile Launcher I"))
        self.assertEquals(m.hardpoint, Hardpoint.MISSILE)

    def test_hardpointNone(self):
        m = Module(db.getItem("Salvager I"))
        self.assertEquals(m.hardpoint, Hardpoint.NONE)

    def test_databaseConsistency(self):
        oldSession = db.saveddata_session
        oldSession.commit()
        try:
            f = Fit()
            f.ship = Ship(db.getItem("Rifter"))
            f.owner = User("moduletest", "testy", False)

            item = db.getItem("Dual Light Pulse Laser I")
            item2 = db.getItem("Stasis Webifier I")
            projMod = Module(item2)
            charge = db.getItem("Gamma S")
            mod = Module(item)
            emptyDummy = Module.buildEmpty(Slot.LOW)
            f.modules.append(emptyDummy)
            posMod1 = Module(item)
            posMod2 = Module(item)
            posMod3 = Module(item)
            posMods = [posMod1, posMod2, posMod3]
            for m in posMods:
                f.modules.append(m)

            mod.charge = charge
            f.modules.append(mod)
            f.projectedModules.append(projMod)
            db.saveddata_session.add(f)
            db.saveddata_session.flush()

            for m in posMods:
                f.modules.remove(m)

            posMods.reverse()
            for m in posMods:
                f.modules.append(m)

            db.saveddata_session.flush()

            #Hack our way through changing the session temporarly
            oldSession = eos.db.saveddata.queries.saveddata_session
            eos.db.saveddata.queries.saveddata_session = sqlalchemy.orm.sessionmaker(bind=db.saveddata_engine)()

            newf = db.getFit(f.ID)
            self.assertNotEquals(id(newf), id(f))

            newmod = newf.modules[1]
            newprojMod = newf.projectedModules[0]
            newdummy = newf.modules[0]

            i = 0
            while i < len(newf.modules):
                if i <= 1:
                    i += 1
                    continue
                else:
                    self.assertEquals(newf.modules[i].ID, posMods[i-2].ID)
                i += 1

            self.assertEquals(newprojMod.item.name, "Stasis Webifier I")
            self.assertNotEquals(id(newprojMod), id(projMod))
            self.assertNotEquals(id(newmod), id(mod))
            self.assertEquals(mod.state, newmod.state)
            self.assertEquals(mod.charge.ID, newmod.charge.ID)
            self.assertEquals(mod.item.ID, newmod.item.ID)

            self.assertEquals(newdummy.slot, emptyDummy.slot)
        except:
            db.saveddata_session.rollback()
            raise
        finally:
            #Undo our hack as to not fuck up anything
            eos.db.saveddata.queries.saveddata_session = oldSession

    def test_copy(self):
        m = Module(db.getItem("Dual Light Pulse Laser I"))
        m.charge = db.getItem("Gamma S")
        m.state = State.OFFLINE

        c = deepcopy(m)

        self.assertNotEquals(id(m), id(c))
        self.assertEquals(m.item, c.item)
        self.assertEquals(m.charge, c.charge)
        self.assertEquals(m.state, c.state)

    def test_maxRange(self):
        m = Module(db.getItem("Remote ECM Burst I"))
        self.assertEquals(m.maxRange, m.getModifiedItemAttr("maxRange"))

        m2 = Module(db.getItem("ECM Burst I"))
        self.assertEquals(m2.maxRange, m2.getModifiedItemAttr("ecmBurstRange"))

        m3 = Module(db.getItem("Standard Missile Launcher I"))
        m3.charge = db.getItem("Bloodclaw Light Missile")
        self.assertEquals(m3.maxRange, 17437.5)

    def test_buildDummy(self):
        m = Module.buildEmpty(Slot.LOW)
        self.assertEquals(m.slot, Slot.LOW)
        self.assertEqual(m.hardpoint, Hardpoint.NONE)

    def test_fitsShipRestriction(self):
        f = Fit()
        m = Module(db.getItem("Judgement"))
        f.ship = Ship(db.getItem("Rifter"))
        self.assertFalse(m.fits(f))

    def test_fitsSlotsFull(self):
        f = Fit()
        f.ship = Ship(db.getItem("Rifter"))
        for _ in xrange(8):
            f.modules.append(Module(db.getItem("Salvager I")))

        self.assertFalse(Module(db.getItem("Salvager I")).fits(f))

    def test_fits(self):
        f = Fit()
        f.ship = Ship(db.getItem("Rifter"))
        self.assertTrue(Module(db.getItem("Salvager I")).fits(f))

    def test_dummyCalc(self):
        m = Module.buildEmpty(Slot.LOW)
        m.calculateModifiedAttributes(Fit(), "normal")

    def test_fits_maxGroupFitted(self):
        f = Fit()
        f.modules.append(Module(db.getItem("Salvager I")))
        m = Module(db.getItem("Damage Control II"))
        f.ship = Ship(db.getItem("Rifter"))
        f.fill()
        self.assertTrue(m.fits(f))

    def test_canHaveState(self):
        f = Fit()
        ab = Module(db.getItem("1MN Afterburner II"))
        ab.state = State.ACTIVE
        mwd = Module(db.getItem("1MN MicroWarpdrive II"))
        mwd.state = State.ACTIVE
        salv = Module(db.getItem("Salvager I"))
        salv.state = State.ACTIVE
        f.modules.append(salv)
        f.modules.append(ab)
        f.modules.append(mwd)
        self.assertFalse(ab.canHaveState(State.ACTIVE))
        self.assertFalse(mwd.canHaveState(State.ACTIVE))
        self.assertTrue(salv.canHaveState(State.ACTIVE))

    def test_numShots(self):
        laser = Module(db.getItem("Dual Giga Pulse Laser I"))
        laser.charge = db.getItem("Multifrequency XL")
        arty = Module(db.getItem("1200mm Artillery Cannon I"))
        arty.charge = db.getItem("Phased Plasma L")
        self.assertEquals(laser.numShots, 0)
        self.assertGreater(arty.numShots, 0)

