from eos.tests import TestBase
from eos import db
from eos.types import Booster, Fit, User, Ship
import sqlalchemy.orm
import eos.db.saveddata.queries
from copy import deepcopy

class Test(TestBase):
    def test_setInvalidBooster(self):
        try:
            Booster(db.getItem("Gamma L"))
        except ValueError:
            return
        self.fail("Expected a ValueError when trying to use Gamma L as a booster")

    def test_setValidBooster(self):
        b = Booster(db.getItem("Strong Drop Booster"))
        self.assertEquals(2, b.slot)
        i = 0
        for _ in b.iterSideEffects():
            i+= 1

        self.assertEquals(4, i)

    def test_testEffectList(self):
        b = Booster(db.getItem("Strong Drop Booster"))
        i = 0
        names = ("boosterTurretFalloffPenalty", "boosterArmorRepairAmountPenalty",
                 "boosterMaxVelocityPenalty", "boosterShieldCapacityPenalty")
        for sideEffect in b.iterSideEffects():
            i += 1
            if not sideEffect.effect.name in names:
                self.fail("Invalid effect " + sideEffect.effect.name)

        self.assertEquals(4, i)

    def test_clear(self):
        b = Booster(db.getItem("Strong Drop Booster"))
        orig = b.getModifiedItemAttr("trackingSpeedMultiplier")

        b.itemModifiedAttributes["trackingSpeedMultiplier"] = 5
        b.clear()
        self.assertEquals(b.getModifiedItemAttr("trackingSpeedMultiplier"), orig)

    def test_databaseConsistency(self):
        oldSession = db.saveddata_session
        oldSession.commit()
        try:
            f = Fit()
            f.ship = Ship(db.getItem("Rifter"))
            f.owner = User("boostertest", "testy", False)
            b = Booster(db.getItem("Strong Drop Booster"))
            b.active = True
            activate = ("boosterTurretFalloffPenalty", "boosterArmorRepairAmountPenalty")
            for sideEffect in b.iterSideEffects():
                if sideEffect.effect.name in activate:
                    sideEffect.active = True

            f.boosters.append(b)
            db.saveddata_session.add(f)
            db.saveddata_session.flush()
            fitID = f.ID
            f1id = id(f)
            b1id = id(b)

            #Hack our way through changing the session temporarly
            oldSession = eos.db.saveddata.queries.saveddata_session
            eos.db.saveddata.queries.saveddata_session = sqlalchemy.orm.sessionmaker(bind=db.saveddata_engine)()

            f = db.getFit(fitID)
            self.assertNotEquals(f1id, id(f))
            i = 0
            for b in f.boosters:
                i += 1
                booster = b

            self.assertTrue(b.active)
            self.assertNotEquals(b1id, id(booster))
            self.assertEquals(i, 1)
            for sideEffect in booster.iterSideEffects():
                    self.assertEquals(sideEffect.effect.name in activate, sideEffect.active)
        except:
            db.saveddata_session.rollback()
            raise
        finally:
            #Undo our hack as to not fuck up anything
            eos.db.saveddata.queries.saveddata_session = oldSession

    def test_copy(self):
        b = Booster(db.getItem("Strong Drop Booster"))
        b.active = False
        activate = ("boosterTurretFalloffPenalty", "boosterArmorRepairAmountPenalty")
        for sideEffect in b.iterSideEffects():
                if sideEffect.effect.name in activate:
                    sideEffect.active = True

        copy = deepcopy(b)

        self.assertNotEquals(id(b), id(copy))
        self.assertEquals(b.item, copy.item)
        self.assertEquals(b.active, copy.active)
        for sideEffect in copy.iterSideEffects():
                    self.assertEquals(sideEffect.effect.name in activate, sideEffect.active)
