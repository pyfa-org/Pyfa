import sys
from os.path import realpath, join, dirname, abspath

from logbook import Logger
pyfalog = Logger(__name__)

debug = False
gamedataCache = True
saveddataCache = True
gamedata_version = ""
gamedata_connectionstring = 'sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "eve.db")), sys.getfilesystemencoding())
pyfalog.debug("Gamedata connection string: {0}", gamedata_connectionstring)

saveddata_connectionstring = 'sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "saveddata", "saveddata.db")), sys.getfilesystemencoding())

pyfalog.debug("Saveddata connection string: {0}", saveddata_connectionstring)

settings = {
    "setting1": True
}

# Autodetect path, only change if the autodetection bugs out.
path = dirname(unicode(__file__, sys.getfilesystemencoding()))
