from eos.tests import TestBase
from eos.modifiedAttributeDict import ModifiedAttributeDict
from eos import db

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.dict = ModifiedAttributeDict()
        self.i = db.getItem("125mm Gatling AutoCannon I")

    def test_setValidOriginal(self):
        self.dict.original = self.i.attributes

    def test_originalAttributesMatch(self):
        self.dict.original = self.i.attributes
        for key,val in self.dict.items():
            self.assertEqual(val, self.i.attributes[key].value)

    def test_modificationWorks(self):
        self.dict.original = self.i.attributes
        self.dict["hp"] = 5
        self.assertEqual(self.dict["hp"], 5)

    def test_overrideAndCalculate(self):
        self.dict.original = self.i.attributes
        self.dict["hp"] = 5
        self.dict.increase("hp", 5)
        self.assertEqual(self.dict["hp"], 10)

    def test_calculateOverride(self):
        self.dict.original = self.i.attributes
        self.dict.increase("hp", 10)
        self.dict["hp"] = 5
        self.assertEqual(self.dict["hp"], 15)

    def test_originalNone(self):
        self.dict.original = {}
        self.assertEquals(self.dict["maeazhtg"], None)

    def test_force(self):
        self.dict.original = self.i.attributes
        self.dict.force("hp", 9000)
        self.dict.increase("hp",284)
        self.dict.multiply("hp", 2487)
        self.dict["hp"] = 1
        self.assertEqual(self.dict["hp"], 9000)

    def test_newValue(self):
        self.dict.original = {}
        self.dict["test"] = 3
        self.dict.increase("test", 5)
        self.assertEqual(self.dict["test"], 8)

    def test_increaseInexistent(self):
        self.dict.original = {}
        self.dict.increase("test", 5)
        self.assertEquals(self.dict["test"], 5)
