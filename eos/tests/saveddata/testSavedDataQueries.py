from eos.tests import TestBase
from eos.types import Fit, Character, User, Ship
from eos import db

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        #Add some test data
        u = User("test", "testy", False)
        c = Character("TESTY")
        c.owner = u
        db.saveddata_session.add(u)
        db.saveddata_session.add(c)
        db.saveddata_session.commit()
        db.saveddata_session.flush()

    def test_1getCharacter(self):
        c = db.getCharacter("TESTY")
        self.assertEquals(c.name, "TESTY")
        self.assertEquals(c.owner.username, "test")

    def test_2getUser(self):
        u = db.getUser("test")
        self.assertEquals(u.username, "test")
        self.assertEqual(len(u.characters), 1)

    def test_3addCharacter(self):
        u = db.getUser("test")
        cc = Character("Testo")
        cc.owner = u
        for char in u.characters:
            if char == cc: return

        self.fail("Didn't find the character we just made")

    def test_4addFit(self):
        u = db.getUser("test")
        f = Fit()
        f.owner = u
        f.shipID = 1 #Set a crap ID so the tests don't fail due to flushing not working due to the not null restriction
        for fit in u.fits:
            if fit == f:
                return

        self.fail("Didn't find the fit we just made")

    def test_5getFitByShipID(self):
        db.saveddata_session.flush()
        l = db.getFitsWithShip(1)
        self.assertEquals(len(l), 1)

    def test_5searchFits(self):
        f = Fit()
        f.ship = Ship(db.getItem("Rifter"))
        f.owner = db.getUser("test")
        f.name = "testety5"
        db.saveddata_session.add(f)
        db.saveddata_session.flush()
        self.assertEquals(len(db.searchFits("testety5")), 1)
