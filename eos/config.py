import sys
from os.path import realpath, join, dirname, abspath

debug = False
gamedataCache = True
saveddataCache = True
gamedata_version = ""
gamedata_connectionstring = 'sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "eve.db")),
                                                   sys.getfilesystemencoding())
saveddata_connectionstring = 'sqlite:///' + unicode(
    realpath(join(dirname(abspath(__file__)), "..", "saveddata", "saveddata.db")), sys.getfilesystemencoding())


# Autodetect path, only change if the autodetection bugs out.
path = dirname(unicode(__file__, sys.getfilesystemencoding()))
