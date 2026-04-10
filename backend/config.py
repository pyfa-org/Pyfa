"""
Mobile-specific config for PYFA backend.

Replaces the root config.py — wx imports and desktop UI colour maps are
removed entirely.  Paths are resolved to Android internal storage conventions
when running on-device; they fall back to local filesystem paths for
development.
"""

import hashlib
import os
import sys
from collections import namedtuple

import yaml
from cryptography.fernet import Fernet
from logbook import (
    CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger,
    NestedSetup, NullHandler, StreamHandler, TimedRotatingFileHandler, WARNING,
)

pyfalog = Logger(__name__)

# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------

debug = False
saveInRoot = False

# ---------------------------------------------------------------------------
# Runtime state (populated by defPaths)
# ---------------------------------------------------------------------------

pyfaPath = None
savePath = None
saveDB = None
gameDB = None
logPath = None
loggingLevel = None
logging_setup = None
cipher = None
clientHash = None
version = None

# ---------------------------------------------------------------------------
# ESI / API server definitions
# ---------------------------------------------------------------------------

ApiServer = namedtuple(
    'ApiServer',
    ['name', 'sso', 'esi', 'client_id', 'callback', 'supports_auto_login'],
)

supported_servers = {
    "Tranquility": ApiServer(
        "Tranquility",
        "login.eveonline.com",
        "esi.evetech.net",
        '095d8cd841ac40b581330919b49fe746',
        # Mobile uses a deep-link redirect, not the GitHub pages callback
        'pyfa-mobile://esi-callback',
        True,
    ),
    "Serenity": ApiServer(
        "Serenity",
        "login.evepc.163.com",
        "ali-esi.evepc.163.com",
        'bc90aa496a404724a93f41b4f4e97761',
        'pyfa-mobile://esi-callback',
        False,
    ),
}

SSO_LOGOFF_SERENITY = 'https://login.evepc.163.com/account/logoff'
ESI_CACHE = 'esi_cache'

minItemSearchLength = 3
minItemSearchLengthCjk = 1


# ---------------------------------------------------------------------------
# Logging level map
# ---------------------------------------------------------------------------

LOGLEVEL_MAP = {
    "critical": CRITICAL,
    "error": ERROR,
    "warning": WARNING,
    "info": INFO,
    "debug": DEBUG,
}


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def getClientSecret():
    return clientHash


def isFrozen():
    return hasattr(sys, 'frozen')


def getPyfaRoot():
    """Return the root directory of the backend package."""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    base = (
        getattr(sys.modules['__main__'], "__file__", sys.executable)
        if isFrozen()
        else __file__
    )
    return os.path.dirname(os.path.realpath(os.path.abspath(base)))


def getVersion():
    return version


def getDefaultSave():
    """
    On Android (Chaquopy) the app's files dir is accessible via
    os.environ['ANDROID_DATA'] or a standard path.  Fall back to ~/.pyfa
    for development.
    """
    android_data = os.environ.get('ANDROID_DATA')
    if android_data:
        return os.path.join(android_data, 'pyfa_mobile')
    return os.path.expanduser(os.path.join("~", ".pyfa_mobile"))


def __createDirs(path):
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def defPaths(customSavePath=None):
    global debug, pyfaPath, savePath, saveDB, gameDB, logPath
    global cipher, clientHash, version

    pyfalog.debug("Configuring PYFA Mobile backend")

    pyfaPath = getPyfaRoot()

    # Version — read from the repo root, two levels up from backend/
    version_file = os.path.join(pyfaPath, '..', 'version.yml')
    if os.path.exists(version_file):
        with open(version_file, 'r') as fh:
            data = yaml.safe_load(fh)
            version = data.get('version', 'unknown')
    else:
        version = 'unknown'

    # User data directory
    if saveInRoot:
        savePath = os.path.join(pyfaPath, "saveddata")
    elif customSavePath:
        savePath = customSavePath
    else:
        savePath = getDefaultSave()

    __createDirs(savePath)

    # Encryption key / client hash (used to scope SSO tokens in the DB)
    secret_file = os.path.join(savePath, ".secret")
    if not os.path.exists(secret_file):
        with open(secret_file, "wb") as fh:
            fh.write(Fernet.generate_key())

    with open(secret_file, 'rb') as fh:
        key = fh.read()
        clientHash = hashlib.sha3_256(key).hexdigest()
        cipher = Fernet(key)

    # Database paths
    saveDB = os.path.join(savePath, "saveddata.db")

    # eve.db lives next to this config file (inside backend/data/)
    data_dir = os.path.join(pyfaPath, "data")
    __createDirs(data_dir)
    gameDB = os.path.join(data_dir, "eve.db")

    # Logging
    logPath = os.path.join(savePath, "pyfa_mobile_debug.log" if debug else "pyfa_mobile.log")

    # Wire up EOS
    import eos.config as eos_config
    eos_config.gamedataCache = False
    eos_config.saveddata_connectionstring = f"sqlite:///{saveDB}?check_same_thread=False"
    eos_config.gamedata_connectionstring = f"sqlite:///{gameDB}?check_same_thread=False"

    from service.settings import EOSSettings
    eos_config.settings = EOSSettings.getInstance().EOSSettings

    pyfalog.debug("savePath: {0}", savePath)
    pyfalog.debug("gameDB:   {0}", gameDB)
    pyfalog.debug("saveDB:   {0}", saveDB)


def defLogging():
    global debug, logPath, loggingLevel, logging_setup

    try:
        if debug:
            logging_setup = NestedSetup([
                NullHandler(),
                StreamHandler(sys.stdout, bubble=False, level=loggingLevel),
                TimedRotatingFileHandler(
                    logPath, level=0, backup_count=3,
                    bubble=True, date_format='%Y-%m-%d',
                ),
            ])
        else:
            logging_setup = NestedSetup([
                NullHandler(),
                FingersCrossedHandler(
                    TimedRotatingFileHandler(
                        logPath, level=0, backup_count=3,
                        bubble=False, date_format='%Y-%m-%d',
                    ),
                    action_level=ERROR,
                    buffer_size=1000,
                ),
            ])
    except Exception:
        logging_setup = NestedSetup([
            NullHandler(),
            StreamHandler(sys.stdout, bubble=False),
        ])
