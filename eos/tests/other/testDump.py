from eos.tests import TestBase
from eos import db

class Test(TestBase):
    def test_unicode(self):
        # Deliberatly request something with non-ASCII symbol in it. Will crash if the dump isn't encoded correctly
        db.getAttributeInfo(384)
