from eos.tests import TestBase
from eos.types import Character, User, Fit, Skill, Ship
from eos.saveddata.character import ReadOnlyException
from eos import db
import eos.db.saveddata.queries
import sqlalchemy.orm
from copy import deepcopy

class Test(TestBase):
    def test_databaseConsistency(self):
        oldSession = db.saveddata_session
        oldSession.commit()
        try:
            f = Fit()
            f.ship = Ship(db.getItem("Rifter"))
            c = Character("testChar")
            f.character = c
            u = User("testChar", "moo", False)
            f.owner = u
            c.owner = u
            c.addSkill(Skill(db.getItem("Caldari Frigate"), 3))
            c.addSkill(Skill(db.getItem("Gallente Frigate"), 1))
            c.addSkill(Skill(db.getItem("Gallente Industrial"), 5))
            db.saveddata_session.add(u)
            db.saveddata_session.add(c)
            db.saveddata_session.add(f)
            db.saveddata_session.flush()

            #Hack our way through changing the session temporarly
            oldSession = eos.db.saveddata.queries.saveddata_session
            eos.db.saveddata.queries.saveddata_session = sqlalchemy.orm.sessionmaker(bind=db.saveddata_engine)()

            newf = db.getFit(f.ID)
            newu = db.getUser(u.ID)
            newc = newu.characters[0]
            self.assertNotEquals(id(newf), id(f))
            self.assertNotEquals(id(newu), id(u))
            self.assertNotEquals(id(newc), id(c))
            self.assertEquals(len(newu.characters), 1)
            self.assertEquals(f.character.ID, newf.character.ID)
            skillDict= {"Caldari Frigate" : 3,
                        "Gallente Frigate" : 1,
                        "Gallente Industrial" : 5}
            for skill in newc.iterSkills():
                self.assertTrue(skillDict.has_key(skill.item.name))
                self.assertEquals(skillDict[skill.item.name], skill.level)


        except:
            db.saveddata_session.rollback()
            raise
        finally:
            #Undo our hack as to not fuck up anything
            eos.db.saveddata.queries.saveddata_session = oldSession

    def test_suppress(self):
        s = Skill(db.getItem("Caldari Frigate"))
        s.suppress()
        self.assertTrue(s.isSuppressed())
        s.clear()
        self.assertFalse(s.isSuppressed())

    def test_getSkill(self):
        c = Character("testetyChar")
        s1 = Skill(db.getItem("Caldari Frigate"), 3)
        c.addSkill(s1)
        c.addSkill(Skill(db.getItem("Gallente Frigate"), 1))
        c.addSkill(Skill(db.getItem("Gallente Industrial"), 5))
        self.assertEquals(c.getSkill(s1.item.name), s1)
        self.assertEquals(c.getSkill(s1.item.ID), s1)
        self.assertEquals(c.getSkill(s1.item), s1)

    def test_readOnly(self):
        s = Skill(db.getItem("Caldari Frigate"), 3, True)
        try:
            s.level = 5
        except ReadOnlyException:
            return
        self.fail("Expected ReadOnlyExcption, didn't get it")

    def test_all0(self):
        c = Character.getAll0()
        for skill in c.iterSkills():
            self.assertEquals(skill.level, 0)

    def test_all5(self):
        c = Character.getAll5()
        for skill in c.iterSkills():
            self.assertEquals(skill.level, 5)

    def test_copy(self):
        c = Character("TEST")
        s = c.getSkill("Leadership")
        s.level = 5
        c.apiKey = "FHIGUUHVBIUHYUIGOYHUIORUIUOHYIUGUIERYGIUUYI9U0BGUYYOIIGHIUHIUYGU"
        c.apiID = 43636

        copy = deepcopy(c)
        self.assertNotEquals(id(c), id(copy))
        self.assertEquals(c.apiKey, copy.apiKey)
        self.assertEquals(c.apiID, copy.apiID)
        self.assertEquals("%s copy" % c.name, copy.name)

        news = copy.getSkill("Leadership")
        self.assertNotEquals(id(s), id(news))
        self.assertEquals(s.level, news.level)
