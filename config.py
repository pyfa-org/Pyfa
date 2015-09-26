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
version = "1.14.1"
tag = "git"
expansionName = "Galatea"
expansionVersion = "1.2"
evemonMinVersion = "4081"

pyfaPath = None
savePath = None
staticPath = None
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

def getPyfaRoot():
    base = sys.executable if isFrozen() else sys.argv[0]
    root = os.path.dirname(os.path.realpath(os.path.abspath(base)))
    root = unicode(root, sys.getfilesystemencoding())
    return root

def __createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def defPaths():
    global debug
    global pyfaPath
    global savePath
    global staticPath
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
        pyfaPath = getPyfaRoot()

    # Where we store the saved fits etc, default is the current users home directory
    if saveInRoot is True:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = os.path.join(pyfaPath, "saveddata")
    else:
        savePath = getattr(configforced, "savePath", None)
        if savePath is None:
            savePath = unicode(os.path.expanduser(os.path.join("~", ".pyfa")),
                               sys.getfilesystemencoding())

    __createDirs(savePath)

    format = '%(asctime)s %(name)-24s %(levelname)-8s %(message)s'
    logging.basicConfig(format=format, level=logLevel)
    handler = logging.handlers.RotatingFileHandler(os.path.join(savePath, "log.txt"), maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)

    logging.info("Starting pyfa")

    if hasattr(sys, 'frozen'):
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl

        # This interferes with cx_Freeze's own handling of exceptions. Find a way to fix this.
        #stderr_logger = logging.getLogger('STDERR')
        #sl = StreamToLogger(stderr_logger, logging.ERROR)
        #sys.stderr = sl


    # Static EVE Data from the staticdata repository, should be in the staticdata
    # directory in our pyfa directory
    staticPath = os.path.join(pyfaPath, "staticdata")

    # The database where we store all the fits etc
    saveDB = os.path.join(savePath, "saveddata.db")

    # The database where the static EVE data from the datadump is kept.
    # This is not the standard sqlite datadump but a modified version created by eos
    # maintenance script
    gameDB = os.path.join(staticPath, "eve.db")

    ## DON'T MODIFY ANYTHING BELOW ##
    import eos.config

    #Caching modifiers, disable all gamedata caching, its unneeded.
    eos.config.gamedataCache = False
    # saveddata db location modifier, shouldn't ever need to touch this
    eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
    eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"
