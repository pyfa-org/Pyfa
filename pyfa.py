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

if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.ensureMinimal('2.8')

from gui import config

# try:
#    import apsw
#    mem = apsw.Connection(":memory:")
#    disk = apsw.Connection(config.gamedata)
#    b = mem.backup("main", disk, "main")
#    try:
#        while not b.done:
#            b.step()
#    finally:
#        b.finish()
#
#    import eos.config
#    import sqlite3
#    conn = sqlite3.connect(mem)
#    eos.config.gamedata_connectionstring = lambda: conn
#    import eos.db
#    eos.db.getItemsByCategory("Skill", eager=("effects", "attributes", "attributes.info.icon", "icon"))
# except:
#    print "failed to use apsw to copy gamedata to memory, prefetching instead"
#    import service.prefetch

import service.prefetch
from gui.mainFrame import MainFrame
import wx
import os
import os.path
import eos.db

if __name__ == "__main__":
    #Make sure the saveddata db exists
    if not os.path.exists(config.savePath):
        os.mkdir(config.savePath)

    eos.db.saveddata_meta.create_all()

    pyfa = wx.App(False)
    MainFrame()
    pyfa.MainLoop()
