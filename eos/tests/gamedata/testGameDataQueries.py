from eos.tests import TestBase
from eos import db
from eos.types import Item

class Test(TestBase):
    def test_getItem(self):
        i = db.getItem("Gamma L")
        self.assertEqual(i.name, "Gamma L")
        self.assertEqual(i.ID, 261)

    def test_searchItems(self):
        i = db.searchItems("Gamma L",where=Item.published == True)
        self.assertEqual(len(i), 7)

    def test_searchItemsWhere(self):
        i = db.searchItems("Gamma L", where=Item.published == False)
        self.assertEqual(len(i), 0)

    def test_getVariations(self):
        i = db.getItem("Gamma L")
        vars = db.getVariations(i)
        for var in vars:
            self.assertEqual(var.metaGroup.parent, i)

    def test_getVariationsMeta(self):
        i = db.getItem("Gamma L")
        vars = db.getVariations(i, metaGroups=4)
        self.assertEquals(len(vars), 5)

    def test_getMarketGroup(self):
        m = db.getMarketGroup(157)
        self.assertEquals(m.name, "Drones")

    def test_getGroup(self):
        g = db.getGroup(920)
        self.assertEquals(g.name, "Effect Beacon")

    def test_getCategory(self):
        c = db.getCategory(6)
        self.assertEquals(c.name, "Ship")

    def test_getAttributeInfo(self):
        i = db.getAttributeInfo(2)
        self.assertEquals(i.name, "isOnline")
