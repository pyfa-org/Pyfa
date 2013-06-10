from eos.tests import TestBase
from eos.types import Ship
from eos import db
from copy import deepcopy

class Test(TestBase):
    def test_clear(self):
        s = Ship(db.getItem("Rifter"))
        orig = s.getModifiedItemAttr("hp")
        s.itemModifiedAttributes["hp"] = 5
        s.clear()
        self.assertEqual(s.getModifiedItemAttr("hp"), orig)

    def test_copy(self):
        s = Ship(db.getItem("Rifter"))
        c = deepcopy(s)

        self.assertNotEquals(id(s), id(c))
        self.assertEquals(s.item, c.item)
