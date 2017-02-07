import sys
from os.path import realpath, join, dirname, abspath

debug = False
gamedataCache = True
saveddataCache = True
gamedata_version = ""

# Autodetect path, only change if the autodetection bugs out.
path = dirname(unicode(__file__, sys.getfilesystemencoding()))
