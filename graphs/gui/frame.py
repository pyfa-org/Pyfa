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
from logbook import Logger

import gui.display
import gui.globalEvents as GE
import gui.mainFrame
from graphs.data.base import FitGraph
from graphs.events import RESIST_MODE_CHANGED
from gui.auxWindow import AuxiliaryFrame
from gui.bitmap_loader import BitmapLoader
from service.const import GraphCacheCleanupReason
from service.settings import GraphSettings
from . import canvasPanel
from .ctrlPanel import GraphControlPanel

pyfalog = Logger(__name__)
_t = wx.GetTranslation


REDRAW_DELAY = 500


class GraphFrame(AuxiliaryFrame):

    def __init__(self, parent, includeHidden=False):
        if not canvasPanel.graphFrame_enabled:
            pyfalog.warning('Matplotlib is not enabled. Skipping initialization.')
            return

        super().__init__(parent, title=_t('Graphs'), size=(520, 390), resizeable=True)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.includeHidden = includeHidden

        self.SetIcon(wx.Icon(BitmapLoader.getBitmap('graphs_small', 'gui')))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Layout - graph selector
        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.graphSelection.Bind(wx.EVT_CHOICE, self.OnGraphSwitched)
        mainSizer.Add(self.graphSelection, 0, wx.EXPAND)

        # Layout - plot area
        self.canvasPanel = canvasPanel.GraphCanvasPanel(self, self)
        mainSizer.Add(self.canvasPanel, 1, wx.EXPAND | wx.ALL, 0)

        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND)

        # Layout - graph control panel
        self.ctrlPanel = GraphControlPanel(self, self)
        mainSizer.Add(self.ctrlPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(mainSizer)

        # Setup - graph selector
        for view in FitGraph.views:
            if view.hidden and not self.includeHidden:
                continue
            self.graphSelection.Append(view.name, view())
        self.graphSelection.SetSelection(0)
        self.ctrlPanel.updateControls(layout=False)

        # Event bindings - local events
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)

        # Event bindings - external events
        self.mainFrame.Bind(GE.FIT_RENAMED, self.OnFitRenamed)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)
        self.mainFrame.Bind(GE.TARGET_PROFILE_RENAMED, self.OnProfileRenamed)
        self.mainFrame.Bind(GE.TARGET_PROFILE_CHANGED, self.OnProfileChanged)
        self.mainFrame.Bind(GE.TARGET_PROFILE_REMOVED, self.OnProfileRemoved)
        self.mainFrame.Bind(RESIST_MODE_CHANGED, self.OnResistModeChanged)
        self.mainFrame.Bind(GE.GRAPH_OPTION_CHANGED, self.OnGraphOptionChanged)
        self.mainFrame.Bind(GE.EFFECTIVE_HP_TOGGLED, self.OnEffectiveHpToggled)

        self.drawTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnDrawTimer, self.drawTimer)

        self.Layout()
        self.UpdateWindowSize()
        self.draw()

    @classmethod
    def openOne(cls, parent, *args, **kwargs):
        if canvasPanel.graphFrame_enabled:
            super().openOne(parent, *args, **kwargs)

    def UpdateWindowSize(self):
        curW, curH = self.GetSize()
        bestW, bestH = self.GetBestSize()
        newW = max(curW, bestW)
        newH = max(curH, bestH)
        if newW > curW or newH > curH:
            newSize = wx.Size(newW, newH)
            self.SetSize(newSize)
            self.SetMinSize(newSize)

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()

    # Fit events
    def OnFitRenamed(self, event):
        event.Skip()
        self.ctrlPanel.OnFitRenamed(event)
        self.draw()

    def OnFitChanged(self, event):
        event.Skip()
        for fitID in event.fitIDs:
            self.clearCache(reason=GraphCacheCleanupReason.fitChanged, extraData=fitID)
        self.ctrlPanel.OnFitChanged(event)
        # Data has to be recalculated - delay redraw
        # to give time to finish UI update in main window
        self.drawTimer.Stop()
        self.drawTimer.Start(REDRAW_DELAY, True)

    def OnFitRemoved(self, event):
        event.Skip()
        self.clearCache(reason=GraphCacheCleanupReason.fitRemoved, extraData=event.fitID)
        self.ctrlPanel.OnFitRemoved(event)
        self.draw()

    # Target profile events
    def OnProfileRenamed(self, event):
        event.Skip()
        self.ctrlPanel.OnProfileRenamed(event)
        self.draw()

    def OnProfileChanged(self, event):
        event.Skip()
        self.clearCache(reason=GraphCacheCleanupReason.profileChanged, extraData=event.profileID)
        self.ctrlPanel.OnProfileChanged(event)
        self.draw()

    def OnProfileRemoved(self, event):
        event.Skip()
        self.clearCache(reason=GraphCacheCleanupReason.profileRemoved, extraData=event.profileID)
        self.ctrlPanel.OnProfileRemoved(event)
        self.draw()

    def OnResistModeChanged(self, event):
        event.Skip()
        for fitID in event.fitIDs:
            self.clearCache(reason=GraphCacheCleanupReason.resistModeChanged, extraData=fitID)
        self.ctrlPanel.OnResistModeChanged(event)
        self.draw()

    def OnGraphOptionChanged(self, event):
        event.Skip()
        layout = getattr(event, 'refreshColumns', False) or getattr(event, 'refreshColumns', False)
        if layout:
            self.ctrlPanel.Freeze()
            if getattr(event, 'refreshAxeLabels', False):
                self.ctrlPanel.refreshAxeLabels(restoreSelection=True)
            if getattr(event, 'refreshColumns', False):
                self.ctrlPanel.refreshColumns()
            self.Layout()
            self.ctrlPanel.Thaw()
        self.clearCache(reason=GraphCacheCleanupReason.optionChanged)
        self.draw()

    def OnEffectiveHpToggled(self, event):
        event.Skip()
        currentView = self.getView()
        # Redraw graph if needed
        if currentView.usesHpEffectivity:
            currentView.isEffective = event.effective
            self.ctrlPanel.refreshAxeLabels(restoreSelection=True)
            self.Layout()
            self.clearCache(reason=GraphCacheCleanupReason.hpEffectivityChanged)
            # Data has to be recalculated - delay redraw
            # to give time to finish UI update in main window
            self.drawTimer.Stop()
            self.drawTimer.Start(REDRAW_DELAY, True)
        # Even if graph is not selected, keep it updated
        for idx in range(self.graphSelection.GetCount()):
            view = self.getView(idx=idx)
            if view is currentView:
                continue
            if view.usesHpEffectivity:
                view.isEffective = event.effective

    def OnGraphSwitched(self, event):
        view = self.getView()
        GraphSettings.getInstance().set('selectedGraph', view.internalName)
        self.clearCache(reason=GraphCacheCleanupReason.graphSwitched)
        self.resetXMark()
        self.ctrlPanel.updateControls()
        self.draw()
        event.Skip()

    def OnDrawTimer(self, event):
        event.Skip()
        self.draw()

    def OnClose(self, event):
        self.mainFrame.Unbind(GE.FIT_RENAMED, handler=self.OnFitRenamed)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        self.mainFrame.Unbind(GE.FIT_REMOVED, handler=self.OnFitRemoved)
        self.mainFrame.Unbind(GE.TARGET_PROFILE_RENAMED, handler=self.OnProfileRenamed)
        self.mainFrame.Unbind(GE.TARGET_PROFILE_CHANGED, handler=self.OnProfileChanged)
        self.mainFrame.Unbind(GE.TARGET_PROFILE_REMOVED, handler=self.OnProfileRemoved)
        self.mainFrame.Unbind(RESIST_MODE_CHANGED, handler=self.OnResistModeChanged)
        self.mainFrame.Unbind(GE.GRAPH_OPTION_CHANGED, handler=self.OnGraphOptionChanged)
        self.mainFrame.Unbind(GE.EFFECTIVE_HP_TOGGLED, handler=self.OnEffectiveHpToggled)
        event.Skip()

    def getView(self, idx=None):
        if idx is None:
            idx = self.graphSelection.GetSelection()
        return self.graphSelection.GetClientData(idx)

    def clearCache(self, reason, extraData=None):
        self.getView().clearCache(reason, extraData)

    def draw(self):
        self.canvasPanel.draw()

    def resetXMark(self):
        self.canvasPanel.xMark = None
