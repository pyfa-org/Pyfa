from eos.tests import TestBase
from eos.types import Price
import time

class Test(TestBase):
    def test_valid(self):
        p = Price(1)
        p.time = time.time() - Price.VALIDITY + 1000
        self.assertTrue(p.isValid)

    def test_invalid(self):
        p = Price(1)
        p.time = time.time() - Price.VALIDITY - 1000
        self.assertFalse(p.isValid)

    def test_newObjectInvalid(self):
        p = Price(1)
        self.assertFalse(p.isValid)
