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

import wx
from gui.statsView import StatsView
import controller
from gui.pyfatogglepanel import TogglePanel
import gui.builtinStatsViews
from gui.builtinStatsViews import *

class StatsPane(wx.Panel):
    DEFAULT_VIEWS = ["exampleView"]

    def fitChanged(self, event):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        for view in self.views:
            view.refreshPanel(fit)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetMinSize((300, -1))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.views = []
        for viewName in self.DEFAULT_VIEWS:
            view = gui.builtinStatsViews.getView(viewName)()
            self.views.append(view)

            tp = TogglePanel(self)
            pane = tp.GetContentPane()

            view.populatePanel(pane)
            tp.SetLabel(view.getHeaderText(None))
            view.refreshPanel(None)

            mainSizer.Add(tp, 0, wx.EXPAND)
