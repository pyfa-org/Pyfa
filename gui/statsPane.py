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

import gui.fittingView as fv
import gui.mainFrame

class StatsPane(wx.Panel):
    DEFAULT_VIEWS = ["resourcesViewFull", "resistancesViewFull" ,"rechargeViewFull", "firepowerViewFull",
                     "capacitorViewFull", "targetingmiscViewFull", "priceViewFull"]

    def fitChanged(self, event):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        for view in self.views:
            view.refreshPanel(fit)
        event.Skip()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetMinSize((310, -1))

        # Force font size 8
        standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        standardFont.SetPointSize(8)
        self.SetFont(standardFont)

#        self.SetBackgroundColour(parent.GetBackgroundColour())

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.views = []
        maxviews = len(self.DEFAULT_VIEWS)
        i=0
        for viewName in self.DEFAULT_VIEWS:
            view = gui.builtinStatsViews.getView(viewName)( self )
            self.views.append(view)

            tp = TogglePanel(self)
            contentPanel = tp.GetContentPane()
            headerPanel = tp.GetHeaderPanel()

            view.populatePanel(contentPanel, headerPanel)
            tp.SetLabel(view.getHeaderText(None))

            view.refreshPanel(None)

            mainSizer.Add(tp, 0, wx.EXPAND | wx.LEFT, 3)
            if i < maxviews - 1:
                mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND | wx.ALL,2)
            i+=1
            tp.OnStateChange(tp.GetBestSize())


        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)
