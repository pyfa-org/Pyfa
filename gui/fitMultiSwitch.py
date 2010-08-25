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
import gui.mainFrame
from gui.fittingView import FittingView
from gui.statsPane import StatsPane
import gui.shipBrowser as sb
import controller

class FitMultiSwitch(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, wx.ID_ANY)
        self.fitPanes = []
        self.AddPage(wx.Panel(self), "+")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.checkAdd)

        self.shipBrowser = gui.mainFrame.MainFrame.getInstance().shipBrowser

        self.shipBrowser.Bind(sb.EVT_FIT_RENAMED, self.processRename)
        self.shipBrowser.Bind(sb.EVT_FIT_SELECTED, self.changeFit)

    def AddTab(self):
        pos = self.GetPageCount() - 1

        p = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        p.view = FittingView(p)
        sizer.Add(p.view, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        p.SetSizer(sizer)

        # Get fit name
        fitID = self.shipBrowser.getSelectedFitID()
        if fitID is None:
            name = "Empty Tab"
        else:
            cFit = controller.Fit.getInstance()
            name = cFit.getFit(fitID).name

        self.InsertPage(pos, p, name)
        wx.CallAfter(self.ChangeSelection, pos)

    def checkAdd(self, event):
        if event.Selection == self.GetPageCount() - 1:
            self.AddTab()
            event.Veto()

    def changeFit(self, event):
        fitID = event.fitID
        cFit = controller.Fit.getInstance()
        selected = self.GetSelection()
        view = self.GetPage(selected).view
        self.SetPageText(selected, cFit.getFit(fitID).name)
        view.changeFit(fitID)

    def processRename(self, event):
        fitID = event.fitID
        cFit = controller.Fit.getInstance()
        for i in xrange(self.GetPageCount() - 1):
            view = self.GetPage(i).view
            if view.activeFitID == fitID:
                self.SetPageText(i, cFit.getFit(fitID).name)
