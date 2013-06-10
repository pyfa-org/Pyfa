import os.path
import sys

debug = False
gamedataCache = True
saveddataCache = True
gamedata_connectionstring = 'sqlite:///' + os.path.expanduser(os.path.join("~", ".pyfa","eve.db"))
saveddata_connectionstring = 'sqlite:///:memory:'

#Autodetect path, only change if the autodetection bugs out.
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
