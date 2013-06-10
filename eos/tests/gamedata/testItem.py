from eos.tests import TestBase
from eos import db
from eos.types import Skill

class Test(TestBase):
    def test_race(self):
        i = db.getItem("Dramiel")
        self.assertEqual(i.race, "angel")

        ii = db.getItem("Punisher")
        self.assertEqual(ii.race, "amarr")

    def test_requiredSkills(self):
        i = db.getItem("Dramiel")
        self.assertEquals(len(i.requiredSkills), 2)
        skills = ("Minmatar Frigate", "Gallente Frigate")
        for skill, level in i.requiredSkills.iteritems():
            self.assertTrue(skill.name in skills)
            self.assertEquals(level, 3)

    def test_requiresSkill(self):
        i = db.getItem("Shield Boost Amplifier II")
        skill = db.getItem("Shield Management")
        self.assertTrue(i.requiresSkill("Shield Management"))
        self.assertTrue(i.requiresSkill("Shield Management", 5))
        self.assertTrue(i.requiresSkill(skill, 5))
        self.assertTrue(i.requiresSkill(skill))
        self.assertFalse(i.requiresSkill(1302))
        self.assertFalse(i.requiresSkill("Moo Management"), 9000)

        self.assertTrue(i.requiresSkill(Skill(skill)))

    def test_attrMover(self):
        i = db.getItem("Rifter")
        self.assertEquals(i.capacity, i.getAttribute("capacity"))
        self.assertEquals(i.volume, i.getAttribute("volume"))
        self.assertEquals(i.mass, i.getAttribute("mass"))
