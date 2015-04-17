from os.path import realpath, join, dirname, abspath
import sys

debug = False
gamedataCache = True
saveddataCache = True
gamedata_connectionstring = 'sqlite:///' + unicode(realpath(join(dirname(abspath(__file__)), "..", "staticdata", "eve.db")), sys.getfilesystemencoding())
saveddata_connectionstring = 'sqlite:///:memory:'

#Autodetect path, only change if the autodetection bugs out.
path = dirname(unicode(__file__, sys.getfilesystemencoding()))
