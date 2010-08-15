import os.path
import sys

#Path autodetection, only change if it doesn't work
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
homePath = os.path.expanduser(os.path.join("~", ".pyfa"))
