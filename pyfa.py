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


import os
import platform
import sys
import traceback
from optparse import AmbiguousOptionError, BadOptionError, OptionParser
from service.prereqsCheck import PreCheckException, version_precheck, version_block
from logbook import CRITICAL, DEBUG, ERROR, FingersCrossedHandler, INFO, Logger, NestedSetup, NullHandler, StreamHandler, TimedRotatingFileHandler, WARNING, \
    __version__ as logbook_version

import config

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

pyfalog = Logger(__name__)


ascii_text = '''
++++++++++++++++++++++++++++++++++++++++++++++++++
                             __       
                            / _|      
              _ __   _   _ | |_  __ _ 
             | '_ \ | | | ||  _|/ _` |
             | |_) || |_| || | | (_| |
             | .__/  \__, ||_|  \__,_|
             | |      __/ |           
             |_|     |___/            

You are running a alpha/beta version of pyfa. 

++++++++++++++++++++++++++++++++++++++++++++++++++
'''

print(ascii_text)

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
                pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)

#
# class LoggerWriter(object):
#     def __init__(self, level):
#         # self.level is really like using log.debug(message)
#         # at least in my case
#         self.level = level
#
#     def write(self, message):
#         # if statement reduces the amount of newlines that are
#         # printed to the logger
#         if message not in {'\n', '    '}:
#             self.level(message.replace("\n", ""))
#
#     def flush(self):
#         # create a flush method so things can be flushed when
#         # the system wants to. Not sure if simply 'printing'
#         # sys.stderr is the correct way to do it, but it seemed
#         # to work properly for me.
#         self.level(sys.stderr)
#
#

def handleGUIException(exc_type, exc_value, exc_traceback):
    try:
        # Try and import wx in case it's missing.
        # noinspection PyPackageRequirements
        import wx
        from gui.errorDialog import ErrorFrame
    except:
        # noinspection PyShadowingNames
        wx = None
        # noinspection PyShadowingNames
        ErrorFrame = None

    tb = traceback.format_tb(exc_traceback)

    try:

        # Try and output to our log handler
        with logging_setup.threadbound():
            module_list = list(set(sys.modules) & set(globals()))
            if module_list:
                pyfalog.info("Imported Python Modules:")
                for imported_module in module_list:
                    module_details = sys.modules[imported_module]
                    pyfalog.info("{0}: {1}", imported_module, getattr(module_details, '__version__', ''))

            pyfalog.critical("Exception in main thread: {0}", str(exc_value))
            # Print the base level traceback
            traceback.print_tb(exc_traceback)

            if wx and ErrorFrame:
                pyfa_gui = wx.App(False)
                if exc_type == PreCheckException:
                    msgbox = wx.MessageBox(str(exc_value), 'Error', wx.ICON_ERROR | wx.STAY_ON_TOP)
                    msgbox.ShowModal()
                else:
                    ErrorFrame(exc_value, tb)

                pyfa_gui.MainLoop()

            pyfalog.info("Exiting.")
    except Exception as ex:
        # Most likely logging isn't available. Try and output to the console
        module_list = list(set(sys.modules) & set(globals()))
        if module_list:
            pyfalog.info("Imported Python Modules:")
            for imported_module in module_list:
                module_details = sys.modules[imported_module]
                print((str(imported_module) + ": " + str(getattr(module_details, '__version__', ''))))

        print(("Exception in main thread: " + str(exc_value)))
        traceback.print_tb(exc_traceback)

        if wx and ErrorFrame:
            pyfa_gui = wx.App(False)
            if exc_type == PreCheckException:
                wx.MessageBox(str(exc_value), 'Error', wx.ICON_ERROR | wx.STAY_ON_TOP)
            else:
                ErrorFrame(exc_value, tb)

            pyfa_gui.MainLoop()

        print("Exiting.")

    finally:
        # TODO: Add cleanup when exiting here.
        pass
        # sys.exit()


# Replace the uncaught exception handler with our own handler.
sys.excepthook = handleGUIException

# Parse command line options
usage = "usage: %prog [--root]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Set logger to debug level.", default=False)
parser.add_option("-t", "--title", action="store", dest="title", help="Set Window Title", default=None)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)
parser.add_option("-l", "--logginglevel", action="store", dest="logginglevel", help="Set desired logging level [Critical|Error|Warning|Info|Debug]", default="Error")

(options, args) = parser.parse_args()
#
# if options.logginglevel == "Critical":
#     options.logginglevel = CRITICAL
# elif options.logginglevel == "Error":
#     options.logginglevel = ERROR
# elif options.logginglevel == "Warning":
#     options.logginglevel = WARNING
# elif options.logginglevel == "Info":
#     options.logginglevel = INFO
# elif options.logginglevel == "Debug":
#     options.logginglevel = DEBUG
# else:
#     options.logginglevel = ERROR

if __name__ == "__main__":
    # Configure paths
    print ('starting')

    version_precheck()

    import wx

    if options.rootsavedata is True:
        config.saveInRoot = True

    # set title if it wasn't supplied by argument
    if options.title is None:
        options.title = "pyfa %s%s - Python Fitting Assistant" % (config.version, "" if config.tag.lower() != 'git' else " (git)")

    config.debug = options.debug
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
        savePath_filename = "Pyfa_debug.log"
    else:
        savePath_filename = "Pyfa.log"

    config.logPath = os.path.join(config.savePath, savePath_filename)

    try:
        if options.debug:
            logging_mode = "Debug"
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                StreamHandler(
                        sys.stdout,
                        bubble=False,
                        level=options.logginglevel
                ),
                TimedRotatingFileHandler(
                        config.logPath,
                        level=0,
                        backup_count=3,
                        bubble=True,
                        date_format='%Y-%m-%d',
                ),
            ])
        else:
            logging_mode = "User"
            logging_setup = NestedSetup([
                # make sure we never bubble up to the stderr handler
                # if we run out of setup handling
                NullHandler(),
                FingersCrossedHandler(
                        TimedRotatingFileHandler(
                                config.logPath,
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
        logging_mode = "Console Only"
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
        pyfalog.info("Starting Pyfa")

        pyfalog.info("Logbook version: {0}", logbook_version)

        pyfalog.info("Running in logging mode: {0}", logging_mode)
        # move this to the log set up - if it fails, can't say that we're writing it
        pyfalog.info("Writing log file to: {0}", config.logPath)

        # Output all stdout (print) messages as warnings
        # try:
        #     sys.stdout = LoggerWriter(pyfalog.warning)
        # except:
        #     pyfalog.critical("Cannot redirect.  Continuing without writing stdout to log.")

        # Output all stderr (stacktrace) messages as critical
        # try:
        #     sys.stderr = LoggerWriter(pyfalog.critical)
        # except:
        #     pyfalog.critical("Cannot redirect.  Continuing without writing stderr to log.")

        if hasattr(sys, 'frozen'):
            pyfalog.info("Running in a frozen state.")
        else:
            pyfalog.info("Running in a thawed state.")

        import eos.db
        import eos.events  # todo: move this to eos initialization

        # noinspection PyUnresolvedReferences
        import service.prefetch  # noqa: F401

        # Make sure the saveddata db exists
        if not os.path.exists(config.savePath):
            os.mkdir(config.savePath)

        eos.db.saveddata_meta.create_all()

        from gui.mainFrame import MainFrame

        pyfa = wx.App(False)
        MainFrame(options.title)
        pyfa.MainLoop()

        # TODO: Add some thread cleanup code here. Right now we bail, and that can lead to orphaned threads or threads not properly exiting.
        sys.exit()
