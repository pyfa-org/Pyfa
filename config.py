import os.path
import sys

debug = False

#Path autodetection, only change if it doesn't work

if hasattr(sys, "frozen"):
    path = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
else:
    path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))

homePath = os.path.expanduser(os.path.join("~", ".pyfa"))
staticPath = homePath
saveddata = os.path.join(homePath, "saveddata.db")

# saveddata db location modifier, shouldn't ever need to touch this
import eos.config
eos.config.saveddata_connectionstring = "sqlite:///" + saveddata
