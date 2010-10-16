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
import bitmapLoader
import gui.mainFrame
import gui.fittingView as fv
import gui.marketBrowser as mb
import gui.shipBrowser as sb
import service

class MultiSwitch(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, wx.ID_ANY)
        self.fitPanes = []
        self.AddPage(wx.Panel(self), "+")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.checkAdd)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.checkRemove)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)
        self.mainFrame.Bind(sb.EVT_FIT_RENAMED, self.processRename)
        self.mainFrame.Bind(sb.EVT_FIT_SELECTED, self.changeFit)
        self.mainFrame.Bind(sb.EVT_FIT_REMOVED, self.processRemove)
        self.mainFrame.Bind(mb.ITEM_SELECTED, self.itemSelected)

        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList)

        self.removal = False
        self.countEvt = 1

    def getActiveFit(self):
        return self.GetCurrentPage().view.activeFitID

    def AddTab(self, type="fit", frame=None, title=None):
        if self.removal:
            self.SetSelection(self.GetPageCount() - 2)
            return False

        #Hide current selection
        pos = self.GetPageCount() - 1

        if type == "fit":
            p = wx.Panel(self)
            p.type = "fit"
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            p.view = fv.FittingView(p)

            sizer.Add(p.view, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

            p.SetSizer(sizer)
            self.InsertPage(pos, p, "")
            self.setTabTitle(pos, None)
        else:
            self.InsertPage(pos, frame, title)
            frame.type=type

        self.SetSelection(pos)
        wx.CallAfter(self.SetSelection, pos)
        return pos

    def removeTab(self, i):
        if self.GetPageCount() > 2:

### FIXME - seems that we remove the wrong image from the list
#            self.ImageList.Remove(self.GetPageImage(i))
###
            self.DeletePage(i)
        else:
            self.setTabTitle(i, None)
            remIcon = self.GetPageImage(i)
            self.SetPageImage(i, -1)
            if remIcon != -1:
                self.ImageList.Remove(remIcon)
            page = self.GetPage(i)
            if page.type == "fit":
                page.view.changeFit(None)

    def checkRemove(self, event):
        tab, _ = self.HitTest(event.Position)
        if tab != -1 and tab != self.GetPageCount() - 1:
            self.removal = True
            self.removeTab(tab)
            #Deleting a tab might have put us on the "+" tab, make sure we don't stay there
            if self.GetSelection() == self.GetPageCount() - 1:
                self.SetSelection(self.GetPageCount() - 2)

            self.removal = False

    def checkAdd(self, event):
        if event.Selection == self.GetPageCount() - 1:
            if "__WXMSW__" not in wx.PlatformInfo:
                self.countEvt = 1

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
                cFit = service.Fit.getInstance()
                fit = cFit.getFit(fitID)
                self.SetPageText(tab, "%s: %s" % (fit.ship.item.name, fit.name))
                bitmap = bitmapLoader.getBitmap("race_%s_small" % fit.ship.item.race, "icons")
                if bitmap:
                    self.SetPageImage(tab, self.imageList.Add(bitmap))

    def pageChanged(self, event):
        #On windows, we can't use the CHANGING event as its bugged, so we need to RECHECK here
        if event.Selection == self.GetPageCount() - 1:
            selection = self.AddTab()
        else:
            selection = event.Selection
            if "__WXMSW__" in wx.PlatformInfo:
                self.countEvt = 0

        page = self.GetPage(selection)

        if self.countEvt == 0:
            if hasattr(page, "type") and page.type == "fit":
                fitID = page.view.activeFitID
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
            else:
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=None))

        self.countEvt -= 1
        if self.countEvt < 0:
            if "__WXMSW__" not in wx.PlatformInfo:
                self.countEvt = 0
            else:
                self.countEvt = 1
        event.Skip()

    def changeFit(self, event):
        selected = self.GetSelection()
        page = self.GetPage(selected)
        if page.type == "fit":
            fitID = event.fitID
            view = page.view
            #Change title of current tab to new fit
            self.setTabTitle(selected, fitID)
            view.changeFit(fitID)

        event.Skip()

    def processRename(self, event):
        fitID = event.fitID
        # Loop through every tab and check if they're our culprit, if so, change tab name
        for i in xrange(self.GetPageCount() - 1):
            page = self.GetPage(i)
            if page.type == "fit":
                view = page.view
                if view.activeFitID == fitID:
                    self.setTabTitle(i, fitID)

        event.Skip()

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

        event.Skip()

    def itemSelected(self, event):
        selected = self.GetSelection()
        page = self.GetPage(selected)
        if page.type == "fit":
            page.view.appendItem(event.itemID)

        event.Skip()
