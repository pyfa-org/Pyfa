import os
import sys
import yaml
import wx

from logbook import CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger, NestedSetup, NullHandler, \
    StreamHandler, TimedRotatingFileHandler, WARNING
import hashlib
from eos.const import FittingSlot

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

evemonMinVersion = "4081"

minItemSearchLength = 3
minItemSearchLengthCjk = 1

pyfaPath = None
savePath = None
saveDB = None
gameDB = None
imgsZIP = None
logPath = None
loggingLevel = None
logging_setup = None
cipher = None
clientHash = None
experimentalFeatures = None
version = None
language = None

API_CLIENT_ID = '095d8cd841ac40b581330919b49fe746'
ESI_CACHE = 'esi_cache'
SSO_CALLBACK = 'https://pyfa-org.github.io/Pyfa/callback'

LOGLEVEL_MAP = {
    "critical": CRITICAL,
    "error": ERROR,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG,
}

CATALOG = 'lang'

slotColourMap = {
    FittingSlot.LOW: wx.Colour(250, 235, 204),  # yellow = low slots
    FittingSlot.MED: wx.Colour(188, 215, 241),  # blue   = mid slots
    FittingSlot.HIGH: wx.Colour(235, 204, 209),  # red    = high slots
    FittingSlot.RIG: '',
    FittingSlot.SUBSYSTEM: ''
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
    return version


def getDefaultSave():
    return os.path.expanduser(os.path.join("~", ".pyfa"))


def defPaths(customSavePath=None):
    global debug
    global pyfaPath
    global savePath
    global saveDB
    global gameDB
    global imgsZIP
    global saveInRoot
    global logPath
    global cipher
    global clientHash
    global version
    global experimentalFeatures
    global language

    pyfalog.debug("Configuring Pyfa")

    # The main pyfa directory which contains run.py
    # Python 2.X uses ANSI by default, so we need to convert the character encoding
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaRoot()

    # Version data

    with open(os.path.join(pyfaPath, "version.yml"), 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
        version = data['version']

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

    imgsZIP = getattr(configforced, "imgsZIP", imgsZIP)
    if not imgsZIP:
        imgsZIP = os.path.join(pyfaPath, "imgs.zip")

    if debug:
        logFile = "pyfa_debug.log"
    else:
        logFile = "pyfa.log"

    logPath = os.path.join(savePath, logFile)

    experimentalFeatures = getattr(configforced, "experimentalFeatures", experimentalFeatures)
    if experimentalFeatures is None:
        experimentalFeatures = False

    # DON'T MODIFY ANYTHING BELOW
    import eos.config

    # Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"

    # initialize the settings
    from service.settings import EOSSettings, LocaleSettings
    eos.config.settings = EOSSettings.getInstance().EOSSettings  # this is kind of confusing, but whatever

    # set langauge, taking the passed argument or falling back to what's saved in the settings
    localeSettings = LocaleSettings.getInstance()
    language = language or localeSettings.get('locale')

    # sets the lang for eos, using the mapped langauge.
    eos.config.set_lang(localeSettings.get_eos_locale())

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
    except (KeyboardInterrupt, SystemExit):
        raise
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


class LoggerWriter:
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
