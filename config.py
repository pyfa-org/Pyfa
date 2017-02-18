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
# Defines if we use a hard set codec or not
# See https://docs.python.org/2/library/codecs.html#standard-encodings
codec = None

# Version data
version = "1.27.0"
tag = "Stable"
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
    pyfaPath = getattr(configforced, "pyfaPath", pyfaPath)
    if pyfaPath is None:
        pyfaPath = getPyfaPath(None, True)

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = getPyfaPath("saveddata", True)
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            if customSavePath is None:  # customSavePath is not overriden
                savePath = os.path.expanduser(os.path.join("~", ".pyfa"))
            else:
                savePath = customSavePath

    savePath = getSavePath(None, True)

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


def getPyfaPath(Append=None, Create=False):
    base = getattr(sys.modules['__main__'], "__file__", sys.executable) if isFrozen() else sys.argv[0]
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    path = parsePath(root, Append, Create)

    if path:
        return path
    else:
        # TODO: add logging and handling when we fail to get a path correctly. Probably should bail and direct the user to how to force the codec.
        return


def getSavePath(Append=None, Create=False):
    root = savePath
    path = parsePath(root, Append, Create)

    if path:
        return path
    else:
        # TODO: add logging and handling when we fail to get a path correctly. Probably should bail and direct the user to how to force the codec.
        return


def parsePath(root, Append=None, Create=False):
    global codec

    if Append:
        root_path = os.path.join(root, Append)
    else:
        root_path = root

    codecs = [
        # Most commonly used
        "utf_8",  # Generic Linux/Mac
        "cp1252",  # Standard Windows
        "cp1251",  # Russian
        # Windows
        "cp037", "cp424", "cp437", "cp500", "cp720", "cp737", "cp775", "cp850", "cp852", "cp855", "cp856", "cp857", "cp858", "cp860", "cp861", "cp862", "cp863",
        "cp864", "cp865", "cp866", "cp869", "cp874", "cp875", "cp932", "cp949", "cp950", "cp1006", "cp1026", "cp1140", "cp1250", "cp1253",
        "cp1254", "cp1255", "cp1256", "cp1257", "cp1258",
        # Mac
        "mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman", "mac_turkish",
        # UTF (universal)
        "utf_16", "utf_32", "utf_32_be", "utf_32_le", "utf_16_be", "utf_16_le", "utf_7", "utf_8_sig",
        # Other (AKA the "weird ones")
        "scii", "big5", "big5hkscs", "euc_jp", "euc_jis_2004", "euc_jisx0213", "euc_kr", "gb2312", "gbk", "gb18030", "hz", "iso2022_jp", "iso2022_jp_1",
        "iso2022_jp_2", "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr", "latin_1", "iso8859_2", "iso8859_3", "iso8859_4", "iso8859_5",
        "iso8859_6", "iso8859_7", "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_11", "iso8859_13", "iso8859_14", "iso8859_15", "iso8859_16", "johab", "koi8_r",
        "koi8_u", "ptcp154", "shift_jis", "shift_jis_2004", "shift_jisx0213"
    ]

    if type(root_path) == str:  # leave unicode ones alone
        path_exists = False

        if codec:
            codec_return = parsePathApplyCodec(root_path, codec)

            if codec_return and Create:
                path_exists = parsePathCreateDir(codec_return)

            if path_exists and os.path.exists(path_exists):
                return codec_return

        for test_codec in codecs:
            codec_return = parsePathApplyCodec(root_path, test_codec)

            if not Create:
                return codec_return

            if codec_return and Create:
                path_exists = parsePathCreateDir(codec_return)

            if path_exists and os.path.exists(path_exists):
                return codec_return
            else:
                continue

        return
    else:
        return root_path


def parsePathApplyCodec(root_path, apply_codec):
    try:
        codec_path = root_path.decode(apply_codec)
    except (UnicodeDecodeError, UnicodeEncodeError, LookupError, UnicodeError, UnicodeTranslateError):
        # TODO: Add logging when we have logbook in place
        codec_path = None

    return codec_path


def parsePathCreateDir(create_path):
    # noinspection PyBroadException
    try:
        if not os.path.exists(create_path):
            os.mkdir(create_path)
        path_exists = True
    except WindowsError:
        path_exists = False
    except Exception:  # as e
        # We got some other error.
        # TODO: Add logging when we have logbook in place
        path_exists = False

    return path_exists
