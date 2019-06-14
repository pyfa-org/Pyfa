# =============================================================================
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
# =============================================================================


# noinspection PyPackageRequirements
import wx

import gui.display


class FitList(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        self.fitList = FitDisplay(self)
        self.mainSizer.Add(self.fitList, 1, wx.EXPAND)
        fitToolTip = wx.ToolTip('Drag a fit into this list to graph it')
        self.fitList.SetToolTip(fitToolTip)


class FitDisplay(gui.display.Display):

    DEFAULT_COLS = ['Base Icon',
                    'Base Name']

    def __init__(self, parent):
        gui.display.Display.__init__(self, parent)


class TargetList(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        self.targetList = TargetDisplay(self)
        self.mainSizer.Add(self.targetList, 1, wx.EXPAND)
        fitToolTip = wx.ToolTip('Drag a fit into this list to graph it')
        self.targetList.SetToolTip(fitToolTip)


class TargetDisplay(gui.display.Display):

    DEFAULT_COLS = ['Base Icon',
                    'Base Name']

    def __init__(self, parent):
        gui.display.Display.__init__(self, parent)
