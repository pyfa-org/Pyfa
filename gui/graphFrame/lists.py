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
import gui.globalEvents as GE
from gui.builtinShipBrowser.events import EVT_FIT_RENAMED
from service.const import GraphCacheCleanupReason
from service.fit import Fit


class BaseList(gui.display.Display):

    DEFAULT_COLS = (
        'Base Icon',
        'Base Name')

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame
        self.fits = []

        self.hoveredRow = None
        self.hoveredColumn = None

        self.defaultTT = 'Drag a fit into this list to graph it'

        self.contextMenu = wx.Menu()
        removeItem = wx.MenuItem(self.contextMenu, 1, 'Remove Fit')
        self.contextMenu.Append(removeItem)
        self.contextMenu.Bind(wx.EVT_MENU, self.ContextMenuHandler, removeItem)

        self.graphFrame.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.graphFrame.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)
        self.graphFrame.mainFrame.Bind(EVT_FIT_RENAMED, self.OnFitRenamed)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == 65 and mstate.GetModifiers() == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and mstate.GetModifiers() == wx.MOD_NONE:
            self.removeFits(self.getSelectedFits())
        event.Skip()

    def OnLeftDClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            try:
                fit = self.fits[row]
            except IndexError:
                pass
            else:
                self.removeFits([fit])

    def OnContextMenu(self, event):
        if self.getSelectedFits():
            self.PopupMenu(self.contextMenu)

    def ContextMenuHandler(self, event):
        selectedMenuItem = event.GetId()
        if selectedMenuItem == 1:
            fits = self.getSelectedFits()
            self.removeFits(fits)

    def OnFitRemoved(self, event):
        event.Skip()
        fit = next((f for f in self.fits if f.ID == event.fitID), None)
        if fit is not None:
            self.removeFits([fit])

    def refreshExtraColumns(self, extraColSpecs):
        baseColNames = set()
        for baseColName in self.DEFAULT_COLS:
            if ":" in baseColName:
                baseColName = baseColName.split(":", 1)[0]
            baseColNames.add(baseColName)
        columnsToRemove = set()
        for col in self.activeColumns:
            if col.name not in baseColNames:
                columnsToRemove.add(col)
        for col in columnsToRemove:
            self.removeColumn(col)
        for colSpec in extraColSpecs:
            self.appendColumnBySpec(colSpec)
        self.refresh(self.fits)

    def OnFitRenamed(self, event):
        event.Skip()
        self.update(self.fits)

    def OnFitChanged(self, event):
        event.Skip()
        if set(event.fitIDs).union(f.ID for f in self.fits):
            self.update(self.fits)

    def getSelectedFits(self):
        fits = []
        for row in self.getSelectedRows():
            try:
                fit = self.fits[row]
            except IndexError:
                continue
            fits.append(fit)
        return fits

    def removeFits(self, fits):
        toRemove = [f for f in fits if f in self.fits]
        if not toRemove:
            return
        for fit in toRemove:
            self.fits.remove(fit)
        self.update(self.fits)
        for fit in fits:
            self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=fit.ID)
        self.graphFrame.draw()

    def unbindExternalEvents(self):
        self.graphFrame.mainFrame.Unbind(GE.FIT_REMOVED, handler=self.OnFitRemoved)
        self.graphFrame.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        self.graphFrame.mainFrame.Unbind(EVT_FIT_RENAMED, handler=self.OnFitRenamed)

    def handleDrag(self, type, fitID):
        if type == 'fit':
            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            if fit not in self.fits:
                self.fits.append(fit)
                self.update(self.fits)
                self.graphFrame.draw()

    def OnLeaveWindow(self, event):
        self.SetToolTip(None)
        self.hoveredRow = None
        self.hoveredColumn = None
        event.Skip()

    def OnMouseMove(self, event):
        row, _, col = self.HitTestSubItem(event.Position)
        if row != self.hoveredRow or col != self.hoveredColumn:
            if self.ToolTip is not None:
                self.SetToolTip(None)
            else:
                self.hoveredRow = row
                self.hoveredColumn = col
                if row != -1 and col != -1 and col < self.ColumnCount:
                    try:
                        fit = self.fits[row]
                    except IndexError:
                        return
                    tooltip = self.activeColumns[col].getToolTip(fit)
                    if tooltip:
                        self.SetToolTip(tooltip)
                    else:
                        self.SetToolTip(None)
                else:
                    self.SetToolTip(self.defaultTT)
        event.Skip()


class FitList(BaseList):

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)
        fit = Fit.getInstance().getFit(self.graphFrame.mainFrame.getActiveFit())
        if fit is not None:
            self.fits.append(fit)
            self.update(self.fits)


class TargetList(BaseList):

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)
        self.update(self.fits)
