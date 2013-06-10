from eos.tests import TestBase
from eos import db

class Test(TestBase):
    def test_attributeNamesMatch(self):
        i = db.getItem("Gamma L")
        for attrName, attr in i.attributes.iteritems():
            self.assertEquals(attrName, attr.name)

    def test_attributeUnit(self):
        a = db.getAttributeInfo("maxVelocity")
        self.assertEquals(a.unit.name, "Acceleration")
        self.assertEquals(a.unit.displayName, "m/sec")
