#!/usr/bin/env python
#===============================================================================
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
#===============================================================================

import sys
import re

if not hasattr(sys, 'frozen'):

    if sys.version_info < (2,6) or sys.version_info > (3,0):
        print("Pyfa requires python 2.x branch ( >= 2.6 )\nExiting.")
        sys.exit(1)

    try:
        import wxversion
    except ImportError:
        print("Cannot find wxPython\nYou can download wxPython (2.8) from http://www.wxpython.org/")
        sys.exit(1)
    try:
        wxversion.select('2.8')
    except wxversion.VersionError:
        try:
            wxversion.ensureMinimal('2.8')
        except wxversion.VersionError:
            print("Installed wxPython version doesn't meet requirements.\nYou can download wxPython (2.8) from http://www.wxpython.org/")
            sys.exit(1)
        else:
            print("wxPython 2.8 not found; attempting to use newer version, expect errors")

    try:
        import sqlalchemy

        saVersion =  sqlalchemy.__version__
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

from optparse import OptionParser

if __name__ == "__main__":
    # Parse command line options
    usage = "usage: %prog [--root]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--root", action="store_true", dest="rootsavedata", help="if you want pyfa to store its data in root folder, use this option", default=False)
    (options, args) = parser.parse_args()

    import config
    # Configure paths
    if options.rootsavedata is True:
        config.saveInRoot = True
    config.defPaths()

    # Import everything
    import wx
    import os
    import os.path

    class PyfaApp(wx.App):
        def __init__(self):
            wx.App.__init__(self, redirect=False)

        def RedirectStdio(self):
            self.stdioWin = self.outputWindowClass()
            sys.stderr = self.stdioWin

    import eos.db
    import service.prefetch

    from gui.mainFrame import MainFrame
    from gui.errorDialog import ErrorWin

    #Make sure the saveddata db exists
    if not os.path.exists(config.savePath):
        os.mkdir(config.savePath)

    eos.db.saveddata_meta.create_all()

    pyfa = PyfaApp()
    pyfa.outputWindowClass = ErrorWin

    # Comment out (or implement flag) to disable GUI error popup
    pyfa.RedirectStdio()

    # Remove comments to debug error window / frame
    # (if it has an error, obviously it won't pop up or log to sys.stderr)
    #dbgErr = ErrorWin()
    #dbgErr.write("Test Error")

    MainFrame(pyfa)
    pyfa.MainLoop()
