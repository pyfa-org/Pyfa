from eos.tests import TestBase
from eos.types import User

class Test(TestBase):
    def testPasswordEncryption(self):
        u = User("MOOBAR")
        u.encodeAndSetPassword("FOOBAR")
        self.assertTrue(u.isPasswordValid("FOOBAR"))
        self.assertFalse(u.isPasswordValid("FOOBUR"))
