from eos.tests import TestBase
from eos import db
import types

class Test(TestBase):
    def test_loadEffect(self):
        i = db.getItem("Rifter")
        self.assertEqual(type(i.effects["shipPDmgBonusMF"].handler), types.FunctionType)
