from eos.tests import TestBase
from eos import db
from eos.types import Module, Hardpoint

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.m = Module(db.getItem("Scan Probe Launcher II"))

    def test_hardpoint(self):
        self.assertEquals(self.m.hardpoint, Hardpoint.NONE)
