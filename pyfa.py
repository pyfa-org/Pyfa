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
        print "Pyfa requires python 2.x branch ( >= 2.6 )\nExiting."
        sys.exit(1)

    try:
        import wxversion
        wxversion.ensureMinimal('2.8')
    except ImportError:
        print "Cannot find wxPython or the installed wxPython version doesn't meet the min. requirements.\nYou can download wxPython (2.8) from http://www.wxpython.org/"
        sys.exit(1)

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
                print "Pyfa requires sqlalchemy 0.5.8 at least  but current sqlalchemy version is %s\nYou can download sqlalchemy (0.5.8+) from http://www.sqlalchemy.org/".format(sqlalchemy.__version__)
                sys.exit(1)
        else:
            print "Unknown sqlalchemy version string format, skipping check"

    except ImportError:
        print "Cannot find sqlalchemy.\nYou can download sqlalchemy (0.6+) from http://www.sqlalchemy.org/"
        sys.exit(1)

import wx
import os
import os.path

import config
import eos.db
import service.prefetch

from gui.mainFrame import MainFrame

if __name__ == "__main__":
    #Make sure the saveddata db exists
    if not os.path.exists(config.savePath):
        os.mkdir(config.savePath)

    eos.db.saveddata_meta.create_all()

    pyfa = wx.App(False)
    MainFrame()
    pyfa.MainLoop()
