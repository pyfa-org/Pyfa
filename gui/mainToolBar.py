#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
from gui import bitmapLoader

class MainToolBar(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, wx.ID_ANY)

        self.AddCheckLabelTool(wx.ID_ANY, "Ship Browser", bitmapLoader.getBitmap("ship_big"))
        self.AddLabelTool(wx.ID_ANY, "Character Editor", bitmapLoader.getBitmap("character_big"))

        self.Realize()
