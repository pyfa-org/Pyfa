import os
import sys

from logbook import CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger, NestedSetup, NullHandler, \
    StreamHandler, TimedRotatingFileHandler, WARNING
import hashlib

from cryptography.fernet import Fernet

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

version = "2.0.1"
tag = "Stable"
expansionName = "YC120.3"
expansionVersion = "1.8"
evemonMinVersion = "4081"

minItemSearchLength = 3

pyfaPath = None
savePath = None
saveDB = None
gameDB = None
logPath = None
loggingLevel = None
logging_setup = None
cipher = None
clientHash = None

ESI_CACHE = 'esi_cache'

LOGLEVEL_MAP = {
    "critical": CRITICAL,
    "error": ERROR,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG,
}


def getClientSecret():
    return clientHash


def isFrozen():
    if hasattr(sys, 'frozen'):
        return True
    else:
        return False


def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getPyfaRoot():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    base = getattr(sys.modules['__main__'], "__file__", sys.executable) if isFrozen() else __file__
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    root = root
    return root


def getVersion():
    if os.path.isfile(os.path.join(pyfaPath, '.version')):
        with open(os.path.join(pyfaPath, '.version')) as f:
            gitVersion = f.readline()
        return gitVersion
    # if no version file exists, then user is running from source or not an official build
    return version + " (git)"


def getDefaultSave():
    return os.path.expanduser(os.path.join("~", ".pyfa"))


def defPaths(customSavePath=None):
    global debug
    global pyfaPath
    global savePath
    global saveDB
    global gameDB
    global saveInRoot
    global logPath
    global cipher
    global clientHash

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

    secret_file = os.path.join(savePath, ".secret")
    if not os.path.exists(secret_file):
        with open(secret_file, "wb") as _file:
            _file.write(Fernet.generate_key())

    with open(secret_file, 'rb') as fp:
        key = fp.read()
        clientHash = hashlib.sha3_256(key).hexdigest()
        cipher = Fernet(key)

    # if isFrozen():
    #    os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(pyfaPath, "cacert.pem")
    #    os.environ["SSL_CERT_FILE"] = os.path.join(pyfaPath, "cacert.pem")

    # The database where we store all the fits etc
    saveDB = os.path.join(savePath, "saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = getattr(configforced, "gameDB", gameDB)
    if not gameDB:
        gameDB = os.path.join(pyfaPath, "eve.db")

    if debug:
        logFile = "pyfa_debug.log"
    else:
        logFile = "pyfa.log"

    logPath = os.path.join(savePath, logFile)

    # DON'T MODIFY ANYTHING BELOW
    import eos.config

    # Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"

    print(eos.config.saveddata_connectionstring)
    print(eos.config.gamedata_connectionstring)

    # initialize the settings
    from service.settings import EOSSettings
    eos.config.settings = EOSSettings.getInstance().EOSSettings  # this is kind of confusing, but whatever


def defLogging():
    global debug
    global logPath
    global loggingLevel
    global logging_setup

    try:
        if debug:
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                StreamHandler(
                        sys.stdout,
                        bubble=False,
                        level=loggingLevel
                ),
                TimedRotatingFileHandler(
                        logPath,
                        level=0,
                        backup_count=3,
                        bubble=True,
                        date_format='%Y-%m-%d',
                ),
            ])
        else:
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                FingersCrossedHandler(
                        TimedRotatingFileHandler(
                                logPath,
                                level=0,
                                backup_count=3,
                                bubble=False,
                                date_format='%Y-%m-%d',
                        ),
                        action_level=ERROR,
                        buffer_size=1000,
                        # pull_information=True,
                        # reset=False,
                )
            ])
    except:
        print("Critical error attempting to setup logging. Falling back to console only.")
        logging_setup = NestedSetup([
            # make sure we never bubble up to the stderr handler
            # if we run out of setup handling
            NullHandler(),
            StreamHandler(
                    sys.stdout,
                    bubble=False
            )
        ])

    with logging_setup.threadbound():

        # Output all stdout (print) messages as warnings
        try:
            sys.stdout = LoggerWriter(pyfalog.warning)
        except:
            pyfalog.critical("Cannot redirect.  Continuing without writing stdout to log.")

        # Output all stderr (stacktrace) messages as critical
        try:
            sys.stderr = LoggerWriter(pyfalog.critical)
        except:
            pyfalog.critical("Cannot redirect.  Continuing without writing stderr to log.")


class LoggerWriter(object):
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message.strip() != '':
            self.level(message.replace("\n", ""))

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)
