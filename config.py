import os.path
import sys

debug = False

#Path autodetection, only change if it doesn't work
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
homePath = os.path.expanduser(os.path.join("~", ".pyfa"))
saveddata = os.path.join(homePath, "saveddata.db")

# saveddata db location modifier, shouldn't ever need to touch this
import eos.config
eos.config.saveddata_connectionstring = "sqlite:///" + saveddata