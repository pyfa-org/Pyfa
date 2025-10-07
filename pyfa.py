#!/usr/bin/env python3
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


import datetime
import os
import sys
from optparse import AmbiguousOptionError, BadOptionError, OptionParser

import config
from service.prereqsCheck import PreCheckException, PreCheckMessage, version_block, version_precheck
from db_update import db_needs_update, update_db


# ascii_text = '''
# ++++++++++++++++++++++++++++++++++++++++++++++++++
#
#                             / _|
#               _ __   _   _ | |
#              | '_ \ | | | ||  _|/ _` |
#              | |_) || |_| || | | (_| |
#              | .__/  \__, ||_|  \__,_|
#              | |      __/ |
#              |_|     |___/
#
# You are running a alpha/beta version of pyfa.
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++
# '''
#
# print(ascii_text)


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
                # pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)


# Parse command line options
usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)
parser.add_option("-t", "--title", action="store", dest="title", help="Set Window Title", default=None)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)
parser.add_option("-l", "--logginglevel", action="store", dest="logginglevel", help="Set desired logging level [Critical|Error|Warning|Info|Debug]", default="Error")
parser.add_option("-p", "--profile", action="store", dest="profile_path", help="Set location to save profileing.", default=None)
parser.add_option("-i", "--language", action="store", dest="language", help="Sets the language for pyfa. Overrides user's saved settings. Format: xx_YY (eg: en_US). If translation doesn't exist, defaults to en_US", default=None)

(options, args) = parser.parse_args()

if __name__ == "__main__":

    try:
        # first and foremost - check required libraries
        version_precheck()
    except PreCheckException as ex:
        # do not pass GO, go directly to jail (and then die =/)
        PreCheckMessage(str(ex))
        sys.exit()

    # from here, we can assume we have the libraries that we need, including wx
    import wx

    from logbook import Logger

    pyfalog = Logger(__name__)

    from gui.errorDialog import ErrorHandler

    # Replace the uncaught exception handler with our own handler.
    sys.excepthook = ErrorHandler.HandleException

    if options.rootsavedata is True:
        config.saveInRoot = True

    config.debug = options.debug
    config.loggingLevel = config.LOGLEVEL_MAP.get(options.logginglevel.lower(), config.LOGLEVEL_MAP['error'])

    config.language = options.language

    config.defPaths(options.savepath)
    config.defLogging()

    with config.logging_setup.applicationbound():

        pyfalog.info("Starting Pyfa")
        pyfalog.info(version_block)

        pyfalog.info("Writing log file to: {0}", config.logPath)

        if hasattr(sys, 'frozen'):
            pyfalog.info("Running in a frozen state.")
        else:
            pyfalog.info("Running in a thawed state.")

        if db_needs_update() is True:
            update_db()

        # Lets get to the good stuff, shall we?
        import eos.db
        import eos.events  # todo: move this to eos initialization?

        # noinspection PyUnresolvedReferences
        import service.prefetch  # noqa: F401

        # Make sure the saveddata db exists
        if not os.path.exists(config.savePath):
            os.mkdir(config.savePath)

        eos.db.saveddata_meta.create_all()
        from gui.app import PyfaApp

        # set title if it wasn't supplied by argument
        if options.title is None:
            options.title = "pyfa %s - Python Fitting Assistant" % (config.getVersion())

        pyfa = PyfaApp(False)

        from gui.mainFrame import MainFrame

        mf = MainFrame(options.title)
        ErrorHandler.SetParent(mf)

        if options.profile_path:
            profile_path = os.path.join(options.profile_path, 'pyfa-{}.profile'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))
            pyfalog.debug("Starting pyfa with a profiler, saving to {}".format(profile_path))
            import cProfile

            cProfile.run('pyfa.MainLoop()', profile_path)
        else:
            pyfa.MainLoop()

        # When main loop is over, threads have 5 seconds to comply...
        import threading
        from utils.timer import CountdownTimer

        timer = CountdownTimer(1)
        stoppableThreads = []
        for t in threading.enumerate():
            if t is not threading.main_thread() and hasattr(t, 'stop'):
                stoppableThreads.append(t)
                t.stop()
        for t in stoppableThreads:
            t.join(timeout=timer.remainder())

        # Nah, just kidding, no way to terminate threads - just try to exit
        sys.exit()
