#!/usr/bin/env python
# ==============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================

import sys
import re
import config

from optparse import OptionParser, BadOptionError, AmbiguousOptionError

from logbook import RotatingFileHandler, Logger, StreamHandler, NestedSetup, FingersCrossedHandler, NullHandler
logger = Logger(__name__)


class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    OSX passes -psn_0_* argument, which is something that pyfa does not handle. See GH issue #423
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                logger.error("Bad startup option passed.")
                largs.append(e.opt_str)


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message not in {'\n', '    '}:
            self.level(message.replace("\n", ""))

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)

# Parse command line options
usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-w", "--wx28", action="store_true", dest="force28", help="Force usage of wxPython 2.8", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)
parser.add_option("-t", "--title", action="store", dest="title", help="Set Window Title", default=None)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)

(options, args) = parser.parse_args()

if not hasattr(sys, 'frozen'):

    if sys.version_info < (2, 6) or sys.version_info > (3, 0):
        print("Pyfa requires python 2.x branch ( >= 2.6 )\nExiting.")
        sys.exit(1)

    try:
        import wxversion
    except ImportError:
        print("Cannot find wxPython\nYou can download wxPython (2.8+) from http://www.wxpython.org/")
        sys.exit(1)

    try:
        if options.force28 is True:
            wxversion.select('2.8')
        else:
            wxversion.select(['3.0', '2.8'])
    except wxversion.VersionError:
        print("Installed wxPython version doesn't meet requirements.\nYou can download wxPython 2.8 or 3.0 from http://www.wxpython.org/")
        sys.exit(1)

    try:
        import sqlalchemy

        saVersion = sqlalchemy.__version__
        saMatch = re.match("([0-9]+).([0-9]+)([b\.])([0-9]+)", saVersion)
        if saMatch:
            saMajor = int(saMatch.group(1))
            saMinor = int(saMatch.group(2))
            betaFlag = True if saMatch.group(3) == "b" else False
            saBuild = int(saMatch.group(4)) if not betaFlag else 0
            if saMajor == 0 and (saMinor < 5 or (saMinor == 5 and saBuild < 8)):
                print("Pyfa requires sqlalchemy 0.5.8 at least  but current sqlalchemy version is %s\nYou can download sqlalchemy (0.5.8+) from http://www.sqlalchemy.org/".format(sqlalchemy.__version__))
                sys.exit(1)
        else:
            print("Unknown sqlalchemy version string format, skipping check")

    except ImportError:
        print("Cannot find sqlalchemy.\nYou can download sqlalchemy (0.6+) from http://www.sqlalchemy.org/")
        sys.exit(1)

    # check also for dateutil module installed.
    try:
        import dateutil.parser  # noqa - Copied import statement from service/update.py
    except ImportError:
        print("Cannot find python-dateutil.\nYou can download python-dateutil from https://pypi.python.org/pypi/python-dateutil")
        sys.exit(1)


if __name__ == "__main__":
    # Configure paths
    if options.rootsavedata is True:
        config.saveInRoot = True

    # set title if it wasn't supplied by argument
    if options.title is None:
        options.title = "pyfa %s%s - Python Fitting Assistant" % (config.version, "" if config.tag.lower() != 'git' else " (git)")

    config.debug = options.debug
    # convert to unicode if it is set
    if options.savepath is not None:
        options.savepath = unicode(options.savepath)
    config.defPaths(options.savepath)

    # Basic logging initialization

    # Logging levels:
    '''
    logbook.CRITICAL
    logbook.ERROR
    logbook.WARNING
    logbook.INFO
    logbook.DEBUG
    logbook.NOTSET
    '''

    if options.debug:
        logging_setup = NestedSetup([
            # make sure we never bubble up to the stderr handler
            # if we run out of setup handling
            NullHandler(),
            StreamHandler(
                sys.stdout,
                bubble=False
            ),
            RotatingFileHandler(
                config.getSavePath("Pyfa_debug.log"),
                level=0,
                max_size=1048576,
                backup_count=5,
                bubble=True
            )
        ])
    else:
        logging_setup = NestedSetup([
            # make sure we never bubble up to the stderr handler
            # if we run out of setup handling
            NullHandler(),
            FingersCrossedHandler(
                RotatingFileHandler(
                    config.getSavePath("Pyfa.log"),
                    level=0,
                    max_size=1048576,
                    backup_count=5,
                    bubble=False
                ),
                # action_level=Warning,
                # buffer_size=1000,
                # pull_information=True,
                # reset=False,
            )
        ])

    with logging_setup.threadbound():
        # Output all stdout (print) messages as warnings
        try:
            sys.stdout = LoggerWriter(logger.warning)
        except ValueError:
            logger.critical("Cannot access log file.  Continuing without writing stdout to log.")
        # Output all stderr (stacktrace) messages as critical
        try:
            sys.stderr = LoggerWriter(logger.critical)
        except ValueError:
            logger.critical("Cannot access log file.  Continuing without writing stderr to log.")

        logger.info("Starting Pyfa")

        # Import everything
        logger.debug("Import wx")
        import wx
        import os
        import os.path

        logger.debug("Import eos.db")
        import eos.db
        import service.prefetch
        from gui.mainFrame import MainFrame

        logger.debug("Make sure the saveddata db exists")
        if not os.path.exists(config.savePath):
            os.mkdir(config.savePath)

        eos.db.saveddata_meta.create_all()

        pyfa = wx.App(False)
        logger.debug("Show GUI")
        MainFrame(options.title)

        # run the gui mainloop
        logger.debug("Run MainLoop()")
        pyfa.MainLoop()
