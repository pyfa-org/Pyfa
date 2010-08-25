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
import bitmapLoader
import gui.mainFrame
from gui.fittingView import FittingView
import gui.shipBrowser as sb
import controller

class MultiSwitch(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, wx.ID_ANY)
        self.fitPanes = []
        self.AddPage(wx.Panel(self), "+")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.checkAdd)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.checkRemove)
        self.shipBrowser = gui.mainFrame.MainFrame.getInstance().shipBrowser

        self.shipBrowser.Bind(sb.EVT_FIT_RENAMED, self.processRename)
        self.shipBrowser.Bind(sb.EVT_FIT_SELECTED, self.changeFit)
        self.shipBrowser.Bind(sb.EVT_FIT_REMOVED, self.processRemove)


        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

    def AddTab(self, type="fit", frame=None, title=None):
        pos = self.GetPageCount() - 1

        if type == "fit":
            p = wx.Panel(self)
            p.type = "fit"
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            p.view = FittingView(p)
            sizer.Add(p.view, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

            p.SetSizer(sizer)

            self.InsertPage(pos, p, "")
            self.setTabTitle(pos, None)
        else:
            self.InsertPage(pos, frame, title)
            frame.type=type

        wx.CallAfter(self.ChangeSelection, pos)

    def removeTab(self, i):
        if self.GetPageCount() > 2:
            self.ImageList.Remove(self.GetPageImage(i))
            self.DeletePage(i)
        else:
            self.setTabTitle(i, None)
            self.SetPageImage(i, -1)
            self.ImageList.Remove(self.GetPageImage(i))

    def checkRemove(self, event):
        tab, _ = self.HitTest(event.Position)
        if tab != -1 and tab != self.GetPageCount() - 1:
            self.removeTab(tab)
            #Deleting a tab might have put us on the "+" tab, make sure we don't stay there
            if self.GetSelection() == self.GetPageCount() - 1:
                self.SetSelection(self.GetPageCount() - 2)

    def checkAdd(self, event):
        if event.Selection == self.GetPageCount() - 1:
            self.AddTab()
            #Veto to prevent the + tab from being selected
            event.Veto()

    def setTabTitle(self, tab, fitID):
        page = self.GetPage(tab)
        if page.type == "fit":
            if fitID == None:
                self.SetPageText(tab, "Empty Tab")
                self.SetPageImage(tab, -1)
            else:
                cFit = controller.Fit.getInstance()
                fit = cFit.getFit(fitID)
                self.SetPageText(tab, "%s: %s" % (fit.ship.item.name, fit.name))
                bitmap = bitmapLoader.getBitmap("race_%s_small" % fit.ship.item.race, "icons")
                imageId = self.imageList.Add(bitmap)
                self.SetPageImage(tab, imageId)

    def changeFit(self, event):
        selected = self.GetSelection()
        page = self.GetPage(selected)
        if page.type == "fit":
            fitID = event.fitID
            view = page.view
            #Change title of current tab to new fit
            self.setTabTitle(selected, fitID)
            view.changeFit(fitID)

    def processRename(self, event):
        fitID = event.fitID
        # Loop through every tab and check if they're our culprit, if so, change tab name
        for i in xrange(self.GetPageCount() - 1):
            page = self.GetPage(i)
            if page.type == "fit":
                view = page.view
                if view.activeFitID == fitID:
                    self.setTabTitle(i, fitID)

    def processRemove(self, event):
        fitID = event.fitID
        for i in xrange(self.GetPageCount() - 2, -1, -1):
            page = self.GetPage(i)
            if page.type == "fit":
                view = page.view
                if view.activeFitID == fitID:
                    self.removeTab(i)


        #Deleting a tab might have put us on the "+" tab, make sure we don't stay there
        if self.GetSelection() == self.GetPageCount() - 1:
            self.SetSelection(self.GetPageCount() - 2)
