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
from eos.saveddata.targetProfile import TargetProfile
from gui.builtinShipBrowser.events import EVT_FIT_RENAMED
from gui.contextMenu import ContextMenu
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

        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.graphFrame.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.graphFrame.mainFrame.Bind(EVT_FIT_RENAMED, self.OnFitRenamed)
        self.graphFrame.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)

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
        self.refreshView()

    def handleDrag(self, type, fitID):
        if type == 'fit':
            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            if fit not in self.fits:
                self.fits.append(fit)
                self.updateView()
                self.graphFrame.draw()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == 65 and mstate.GetModifiers() == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and mstate.GetModifiers() == wx.MOD_NONE:
            self.removeListItems(self.getSelectedListItems())
        event.Skip()

    def OnLeftDClick(self, event):
        row, _ = self.HitTest(event.Position)
        item = self.getListItem(row)
        if item is None:
            return
        self.removeListItems([item])

    def OnFitRenamed(self, event):
        event.Skip()
        self.updateView()

    def OnFitChanged(self, event):
        event.Skip()
        if set(event.fitIDs).union(f.ID for f in self.fits):
            self.updateView()

    def OnFitRemoved(self, event):
        event.Skip()
        fit = next((f for f in self.fits if f.ID == event.fitID), None)
        if fit is not None:
            self.removeListItems([fit])

    def OnMouseMove(self, event):
        row, _, col = self.HitTestSubItem(event.Position)
        if row != self.hoveredRow or col != self.hoveredColumn:
            if self.ToolTip is not None:
                self.SetToolTip(None)
            else:
                self.hoveredRow = row
                self.hoveredColumn = col
                if row != -1 and col != -1 and col < self.ColumnCount:
                    item = self.getListItem(row)
                    if item is None:
                        return
                    tooltip = self.activeColumns[col].getToolTip(item)
                    if tooltip:
                        self.SetToolTip(tooltip)
                    else:
                        self.SetToolTip(None)
                else:
                    self.SetToolTip(self.defaultTTText)
        event.Skip()

    def OnLeaveWindow(self, event):
        self.SetToolTip(None)
        self.hoveredRow = None
        self.hoveredColumn = None
        event.Skip()

    @property
    def defaultTTText(self):
        raise NotImplementedError

    def refreshView(self):
        raise NotImplementedError

    def updateView(self):
        raise NotImplementedError

    def getListItem(self, row):
        raise NotImplementedError

    def removeListItems(self, items):
        raise NotImplementedError

    def getSelectedListItems(self):
        items = []
        for row in self.getSelectedRows():
            item = self.getListItem(row)
            if item is None:
                continue
            items.append(item)
        return items

    def unbindExternalEvents(self):
        self.graphFrame.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        self.graphFrame.mainFrame.Unbind(EVT_FIT_RENAMED, handler=self.OnFitRenamed)
        self.graphFrame.mainFrame.Unbind(GE.FIT_REMOVED, handler=self.OnFitRemoved)


class FitList(BaseList):

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        fit = Fit.getInstance().getFit(self.graphFrame.mainFrame.getActiveFit())
        if fit is not None:
            self.fits.append(fit)
            self.updateView()

    def refreshView(self):
        self.refresh(self.fits)

    def updateView(self):
        self.update(self.fits)

    def spawnMenu(self, event):
        selection = self.getSelectedListItems()
        clickedPos = self.getRowByAbs(event.Position)
        mainItem = self.getListItem(clickedPos)

        sourceContext = 'graphFitList'
        itemContext = None if mainItem is None else 'Fit'
        menu = ContextMenu.getMenu(self, mainItem, selection, (sourceContext, itemContext))
        if menu:
            self.PopupMenu(menu)

    def getListItem(self, row):
        if row == -1:
            return None
        try:
            return self.fits[row]
        except IndexError:
            return None

    def removeListItems(self, items):
        toRemove = [i for i in items if i in self.fits]
        if not toRemove:
            return
        for fit in toRemove:
            self.fits.remove(fit)
        self.updateView()
        for fit in toRemove:
            self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=fit.ID)
        self.graphFrame.draw()

    @property
    def defaultTTText(self):
        return  'Drag a fit into this list to graph it'


class TargetList(BaseList):

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)
        
        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.profiles = []
        self.profiles.append(TargetProfile.getIdeal())
        self.updateView()

    def refreshView(self):
        self.refresh(self.targets)

    def updateView(self):
        self.update(self.targets)

    def spawnMenu(self, event):
        selection = self.getSelectedListItems()
        clickedPos = self.getRowByAbs(event.Position)
        mainItem = self.getListItem(clickedPos)

        sourceContext = 'graphTgtList'
        itemContext = None if mainItem is None else 'Target'
        menu = ContextMenu.getMenu(self, mainItem, selection, (sourceContext, itemContext))
        if menu:
            self.PopupMenu(menu)

    def getListItem(self, row):
        if row == -1:
            return None

        numFits = len(self.fits)
        numProfiles = len(self.profiles)

        if (numFits + numProfiles) == 0:
            return None

        if row < numFits:
            return self.fits[row]
        else:
            return self.profiles[row - numFits]

    def removeListItems(self, items):
        fitsToRemove = [i for i in items if i in self.fits]
        profilesToRemove = [i for i in items if i in self.profiles]
        if not fitsToRemove and not profilesToRemove:
            return
        for fit in fitsToRemove:
            self.fits.remove(fit)
        for profile in profilesToRemove:
            self.profiles.remove(profile)
        self.updateView()
        for fit in fitsToRemove:
            self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=fit.ID)
        for profile in profilesToRemove:
            self.graphFrame.clearCache(reason=GraphCacheCleanupReason.profileRemoved, extraData=profile.ID)
        self.graphFrame.draw()

    @property
    def targets(self):
        return self.fits + self.profiles

    @property
    def defaultTTText(self):
        return  'Drag a fit into this list to have your fits graphed against it'
