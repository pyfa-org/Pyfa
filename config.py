import os
import sys

# TODO: move all logging back to pyfa.py main loop
# We moved it here just to avoid rebuilding windows skeleton for now (any change to pyfa.py needs it)
import logging
import logging.handlers

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
version = "1.27.1"
tag = "git"
expansionName = "YC119.2"
expansionVersion = "1.2"
evemonMinVersion = "4081"

pyfaPath = None
savePath = None
saveDB = None
gameDB = None


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    From: http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


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

    if debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.WARN

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

    loggingFormat = '%(asctime)s %(name)-24s %(levelname)-8s %(message)s'
    logging.basicConfig(format=loggingFormat, level=logLevel)
    handler = logging.handlers.RotatingFileHandler(getSavePath("log.txt"), maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter(loggingFormat)
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)

    logging.info("Starting pyfa")

    if hasattr(sys, 'frozen'):
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl

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
