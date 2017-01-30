import os
import sys

from logbook import Logger
logger = Logger(__name__)

# Load variable overrides specific to distribution type
try:
    import configforced
except ImportError:
    configforced = None

# Turns on debug mode
debug = False
# Defines if our saveddata will be in pyfa root or not
saveInRoot = False

# Version data
version = "1.26.1"
tag = "git"
expansionName = "YC118.10"
expansionVersion = "1.2"
evemonMinVersion = "4081"

pyfaPath = None
savePath = None
saveDB = None
gameDB = None

def isFrozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False


def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def defPaths(customSavePath):
    global debug
    global pyfaPath
    global savePath
    global saveDB
    global gameDB
    global saveInRoot

    logger.debug("Configuring Pyfa")

    # The main pyfa directory which contains run.py
    # Python 2.X uses ANSI by default, so we need to convert the character encoding
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaPath()

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = getPyfaPath("saveddata")
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            if customSavePath is None:  # customSavePath is not overriden
                savePath = os.path.expanduser(os.path.join("~", ".pyfa"))
            else:
                savePath = customSavePath

    __createDirs(savePath)

    if isFrozen():
        certName = "cacert.pem"
        os.environ["REQUESTS_CA_BUNDLE"] = getPyfaPath(certName).encode('utf8')
        os.environ["SSL_CERT_FILE"] = getPyfaPath(certName).encode('utf8')


    if hasattr(sys, 'frozen'):
        pass

        # This interferes with cx_Freeze's own handling of exceptions. Find a way to fix this.
        # stderr_logger = logging.getLogger('STDERR')
        # sl = StreamToLogger(stderr_logger, logging.ERROR)
        # sys.stderr = sl

    # The database where we store all the fits etc
    saveDB = getSavePath("saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = getPyfaPath("eve.db")

    # DON'T MODIFY ANYTHING BELOW!
    import eos.config

    # Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"


def getPyfaPath(Append=None):
    base = getattr(sys.modules['__main__'], "__file__", sys.executable) if isFrozen() else sys.argv[0]
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))

    if Append:
        path = parsePath(root, Append)
    else:
        path = parsePath(root)

    return path


def getSavePath(Append=None):
    root = savePath

    if Append:
        path = parsePath(root, Append)
    else:
        path = parsePath(root)

    return path


def parsePath(root, Append=None):
    if Append:
        path = os.path.join(root, Append)
    else:
        path = root

    if type(path) == str:  # leave unicode ones alone
        try:
            path = path.decode('utf8')
        except UnicodeDecodeError:
            path = path.decode('windows-1252')

    return path
