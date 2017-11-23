import os
import sys

from logbook import Logger

pyfalog = Logger(__name__)

# Load variable overrides specific to distribution type
try:
    import configforced
except ImportError:
    pyfalog.warning("Failed to import: configforced")
    configforced = None


# Turns on debug mode
debug = False
# Defines if our saveddata will be in pyfa root or not
saveInRoot = False

# Version data
version = "1.33.3"
tag = "git"
expansionName = "Lifeblood"
expansionVersion = "1.7"
evemonMinVersion = "4081"

pyfaPath = None
savePath = None
saveDB = None
gameDB = None
logPath = None


def isFrozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False


def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getPyfaRoot():
    base = getattr(sys.modules['__main__'], "__file__", sys.executable) if isFrozen() else sys.argv[0]
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    root = unicode(root, sys.getfilesystemencoding())
    return root


def getDefaultSave():
    return unicode(os.path.expanduser(os.path.join("~", ".pyfa")), sys.getfilesystemencoding())


def defPaths(customSavePath):
    global debug
    global pyfaPath
    global savePath
    global saveDB
    global gameDB
    global saveInRoot

    pyfalog.debug("Configuring Pyfa")

    # The main pyfa directory which contains run.py
    # Python 2.X uses ANSI by default, so we need to convert the character encoding
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaRoot()

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = os.path.join(pyfaPath, "saveddata")
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            if customSavePath is None:  # customSavePath is not overriden
                savePath = getDefaultSave()
            else:
                savePath = customSavePath

    __createDirs(savePath)

    if isFrozen():
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(pyfaPath, "cacert.pem").encode('utf8')
        os.environ["SSL_CERT_FILE"] = os.path.join(pyfaPath, "cacert.pem").encode('utf8')

    # The database where we store all the fits etc
    saveDB = os.path.join(savePath, "saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = getattr(configforced, "gameDB", gameDB)
    if not gameDB:
        gameDB = os.path.join(pyfaPath, "eve.db")

    # DON'T MODIFY ANYTHING BELOW
    import eos.config

    # Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"

    # initialize the settings
    from service.settings import EOSSettings
    eos.config.settings = EOSSettings.getInstance().EOSSettings  # this is kind of confusing, but whatever
