#!/usr/bin/env python
#===============================================================================
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import unittest, os.path, sys

#Add the good path to sys.path
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..", "..")))

from eos import config

config.debug = False
config.saveddata_connectionstring = "sqlite:///:memory:"
config.saveddataCache = None

class Loader(unittest.TestLoader):
    def loadTestsFromName(self, name, module = None):
        if name == "discover":
            return iteratedir(os.path.dirname(__file__))
        else:
            prefix = name.split(".")
            fullpath = os.path.join(os.path.dirname(__file__), *prefix)
            if os.path.isdir(os.path.join(fullpath)):
                return iteratedir(fullpath, prefix)
            else:
                module = __import__(name, fromlist=True)
                return self.loadTestsFromModule(module)

loader = Loader()
def iteratedir(dir, prefix = [], suite = None):
    suite = suite if suite is not None else unittest.TestSuite()
    for filename in os.listdir(dir or '.'):
        moduleName, ext = os.path.splitext(filename)
        moduleName = '.'.join(prefix + [moduleName])

        if os.path.isdir(os.path.join(dir, filename)):
            module = __import__(moduleName + ".__init__", fromlist = True)
            subSuite = unittest.TestSuite()
            suite.addTest(subSuite)
            iteratedir(os.path.join(dir, filename), prefix + [filename], subSuite)

        if ext == ".py" and moduleName not in ("__init__", "runTests", "runMassEffectTests"):
            module = __import__(moduleName, fromlist = True)
            suite.addTest(loader.loadTestsFromModule(module))

    return suite

if __name__ == "__main__":
    unittest.main(defaultTest="discover", testLoader=loader)
