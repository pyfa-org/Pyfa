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
from eos.saveddata.targetProfile import TargetProfile
from graphs.wrapper import SourceWrapper, TargetWrapper
from gui.contextMenu import ContextMenu
from service.const import GraphCacheCleanupReason
from service.fit import Fit


class BaseWrapperList(gui.display.Display):

    DEFAULT_COLS = (
        'Base Icon',
        'Base Name')

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame
        self._wrappers = []

        self.hoveredRow = None
        self.hoveredColumn = None

        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    @property
    def wrappers(self):
        return sorted(self._wrappers, key=lambda w: w.isFit)

    # UI-related stuff
    @property
    def defaultTTText(self):
        raise NotImplementedError

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

    def refreshView(self):
        self.refresh(self.wrappers)

    def updateView(self):
        self.update(self.wrappers)

    # UI event handling
    def OnMouseMove(self, event):
        row, _, col = self.HitTestSubItem(event.Position)
        if row != self.hoveredRow or col != self.hoveredColumn:
            if self.ToolTip is not None:
                self.SetToolTip(None)
            else:
                self.hoveredRow = row
                self.hoveredColumn = col
                if row != -1 and col != -1 and col < self.ColumnCount:
                    item = self.getWrapper(row)
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

    def handleDrag(self, type, fitID):
        if type == 'fit' and not self.containsFitID(fitID):
            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            self.appendItem(fit)
            self.updateView()
            self.graphFrame.draw()

    def OnLeftDClick(self, event):
        row, _ = self.HitTest(event.Position)
        wrapper = self.getWrapper(row)
        if wrapper is None:
            return
        self.removeWrappers([wrapper])

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == 65 and mstate.GetModifiers() == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and mstate.GetModifiers() == wx.MOD_NONE:
            self.removeWrappers(self.getSelectedWrappers())
        event.Skip()

    # Wrapper-related methods
    @property
    def wrapperClass(self):
        raise NotImplementedError

    def getWrapper(self, row):
        if row == -1:
            return None
        try:
            return self._wrappers[row]
        except IndexError:
            return None

    def removeWrappers(self, wrappers):
        wrappers = set(wrappers).union(self._wrappers)
        if not wrappers:
            return
        for wrapper in wrappers:
            self._wrappers.remove(wrapper)
        self.updateView()
        for wrapper in wrappers:
            if wrapper.isFit:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=wrapper.item.ID)
            elif wrapper.isProfile:
                self.graphFrame.clearCache(reason=GraphCacheCleanupReason.profileRemoved, extraData=wrapper.item.ID)
        self.graphFrame.draw()

    def getSelectedWrappers(self):
        wrappers = []
        for row in self.getSelectedRows():
            wrapper = self.getWrapper(row)
            if wrapper is None:
                continue
            wrappers.append(wrapper)
        return wrappers

    def appendItem(self, item):
        self._wrappers.append(self.wrapperClass(item))

    def containsFitID(self, fitID):
        for wrapper in self._wrappers:
            if wrapper.isFit and wrapper.item.ID == fitID:
                return True
        return False

    def containsProfileID(self, profileID):
        for wrapper in self._wrappers:
            if wrapper.isProfile and wrapper.item.ID == profileID:
                return True
        return False

    # Wrapper-related events
    def OnFitRenamed(self, event):
        if self.containsFitID(event.fitID):
            self.updateView()

    def OnFitChanged(self, event):
        if set(event.fitIDs).union(w.item.ID for w in self._wrappers if w.isFit):
            self.updateView()

    def OnFitRemoved(self, event):
        wrapper = next((w for w in self._wrappers if w.isFit and w.item.ID == event.fitID), None)
        if wrapper is not None:
            self._wrappers.remove(wrapper)
            self.updateView()

    def OnProfileRenamed(self, event):
        if self.containsProfileID(event.profileID):
            self.updateView()

    def OnProfileChanged(self, event):
        if self.containsProfileID(event.profileID):
            self.updateView()

    def OnProfileRemoved(self, event):
        wrapper = next((w for w in self._wrappers if w.isProfile and w.item.ID == event.profileID), None)
        if wrapper is not None:
            self._wrappers.remove(wrapper)
            self.updateView()

    # Context menu handlers
    def addFit(self, fit):
        if fit is None:
            return
        if self.containsFitID(fit.ID):
            return
        self.appendItem(fit)
        self.updateView()
        self.graphFrame.draw()

    def getExistingFitIDs(self):
        return [w.item.ID for w in self._wrappers if w.isFit]

    def addFitsByIDs(self, fitIDs):
        sFit = Fit.getInstance()
        for fitID in fitIDs:
            if self.containsFitID(fitID):
                continue
            fit = sFit.getFit(fitID)
            if fit is not None:
                self.appendItem(fit)
        self.updateView()
        self.graphFrame.draw()


class SourceWrapperList(BaseWrapperList):

    wrapperClass = SourceWrapper

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        fit = Fit.getInstance().getFit(self.graphFrame.mainFrame.getActiveFit())
        if fit is not None:
            self.appendItem(fit)
            self.updateView()

    def spawnMenu(self, event):
        selection = self.getSelectedWrappers()
        clickedPos = self.getRowByAbs(event.Position)
        mainItem = self.getWrapper(clickedPos)

        sourceContext = 'graphFitList'
        itemContext = None if mainItem is None else 'Fit'
        menu = ContextMenu.getMenu(self, mainItem, selection, (sourceContext, itemContext))
        if menu:
            self.PopupMenu(menu)

    @property
    def defaultTTText(self):
        return 'Drag a fit into this list to graph it'


class TargetWrapperList(BaseWrapperList):

    wrapperClass = TargetWrapper

    def __init__(self, graphFrame, parent):
        super().__init__(graphFrame, parent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.appendItem(TargetProfile.getIdeal())
        self.updateView()

    def spawnMenu(self, event):
        selection = self.getSelectedWrappers()
        clickedPos = self.getRowByAbs(event.Position)
        mainItem = self.getWrapper(clickedPos)

        sourceContext = 'graphTgtList'
        itemContext = None if mainItem is None else 'Target'
        menu = ContextMenu.getMenu(self, mainItem, selection, (sourceContext, itemContext))
        if menu:
            self.PopupMenu(menu)

    @property
    def defaultTTText(self):
        return 'Drag a fit into this list to have your fits graphed against it'

    # Context menu handlers
    def addProfile(self, profile):
        if profile is None:
            return
        if self.containsProfileID(profile.ID):
            return
        self.appendItem(profile)
        self.updateView()
        self.graphFrame.draw()
