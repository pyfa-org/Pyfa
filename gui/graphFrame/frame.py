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


import itertools
import os
import traceback

# noinspection PyPackageRequirements
import wx
from logbook import Logger

import gui.display
import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.builtinGraphs.base import FitGraph
from gui.builtinShipBrowser.events import EVT_FIT_RENAMED
from service.const import GraphCacheCleanupReason
from service.settings import GraphSettings
from .panel import GraphControlPanel


pyfalog = Logger(__name__)

try:
    import matplotlib as mpl

    mpl_version = int(mpl.__version__[0]) or -1
    if mpl_version >= 2:
        mpl.use('wxagg')
        graphFrame_enabled = True
    else:
        graphFrame_enabled = False

    from matplotlib.patches import Patch
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    from matplotlib.figure import Figure
except ImportError as e:
    pyfalog.warning('Matplotlib failed to import.  Likely missing or incompatible version.')
    graphFrame_enabled = False
except Exception:
    # We can get exceptions deep within matplotlib. Catch those.  See GH #1046
    tb = traceback.format_exc()
    pyfalog.critical('Exception when importing Matplotlib. Continuing without importing.')
    pyfalog.critical(tb)
    graphFrame_enabled = False


class GraphFrame(wx.Frame):

    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FRAME_FLOAT_ON_PARENT):

        global graphFrame_enabled
        if not graphFrame_enabled:
            pyfalog.warning('Matplotlib is not enabled. Skipping initialization.')
            return

        wx.Frame.__init__(self, parent, title='pyfa: Graph Generator', style=style, size=(520, 390))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.SetIcon(wx.Icon(BitmapLoader.getBitmap('graphs_small', 'gui')))

        # Remove matplotlib font cache, see #234
        try:
            cache_dir = mpl._get_cachedir()
        except:
            cache_dir = os.path.expanduser(os.path.join('~', '.matplotlib'))
        cache_file = os.path.join(cache_dir, 'fontList.cache')
        if os.access(cache_dir, os.W_OK | os.X_OK) and os.path.isfile(cache_file):
            os.remove(cache_file)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Layout - graph selector
        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.graphSelection.Bind(wx.EVT_CHOICE, self.OnGraphSwitched)
        mainSizer.Add(self.graphSelection, 0, wx.EXPAND)

        # Layout - plot area
        self.figure = Figure(figsize=(5, 3), tight_layout={'pad': 1.08})
        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        clr = [c / 255. for c in rgbtuple]
        self.figure.set_facecolor(clr)
        self.figure.set_edgecolor(clr)
        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))
        self.subplot = self.figure.add_subplot(111)
        self.subplot.grid(True)
        mainSizer.Add(self.canvas, 1, wx.EXPAND)

        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND)

        # Layout - graph control panel
        self.ctrlPanel = GraphControlPanel(self, self)
        mainSizer.Add(self.ctrlPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(mainSizer)

        # Setup - graph selector
        for view in FitGraph.views:
            self.graphSelection.Append(view.name, view())
        self.graphSelection.SetSelection(0)
        self.ctrlPanel.updateControls(layout=False)

        # Event bindings - local events
        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        # Event bindings - external events
        self.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.mainFrame.Bind(EVT_FIT_RENAMED, self.OnFitRenamed)
        self.mainFrame.Bind(GE.GRAPH_OPTION_CHANGED, self.OnGraphOptionChanged)

        self.Layout()
        self.UpdateWindowSize()
        self.draw()

    def UpdateWindowSize(self):
        curW, curH = self.GetSize()
        bestW, bestH = self.GetBestSize()
        newW = max(curW, bestW)
        newH = max(curH, bestH)
        if newW > curW or newH > curH:
            newSize = wx.Size(newW, newH)
            self.SetSize(newSize)
            self.SetMinSize(newSize)

    def closeEvent(self, event):
        self.closeWindow()
        event.Skip()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == wx.WXK_ESCAPE and mstate.GetModifiers() == wx.MOD_NONE:
            self.closeWindow()
            return
        event.Skip()

    def OnFitChanged(self, event):
        event.Skip()
        self.clearCache(reason=GraphCacheCleanupReason.fitChanged, extraData=event.fitID)
        self.draw()

    def OnFitRenamed(self, event):
        event.Skip()
        self.draw()

    def OnGraphOptionChanged(self, event):
        event.Skip()
        self.clearCache(reason=GraphCacheCleanupReason.optionChanged)
        self.draw()

    def OnGraphSwitched(self, event):
        view = self.getView()
        GraphSettings.getInstance().set('selectedGraph', view.internalName)
        self.clearCache(reason=GraphCacheCleanupReason.graphSwitched)
        self.ctrlPanel.updateControls()
        self.draw()
        event.Skip()

    def closeWindow(self):
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        self.mainFrame.Unbind(EVT_FIT_RENAMED, handler=self.OnFitRenamed)
        self.mainFrame.Unbind(GE.GRAPH_OPTION_CHANGED, handler=self.OnGraphOptionChanged)
        self.ctrlPanel.unbindExternalEvents()
        self.Destroy()

    def getView(self):
        return self.graphSelection.GetClientData(self.graphSelection.GetSelection())

    def clearCache(self, reason, extraData=None):
        self.getView().clearCache(reason, extraData)

    def draw(self):
        global mpl_version

        # Eee #1430. draw() is not being unbound properly when the window closes.
        # This is an easy fix, but not a proper solution
        if not self:
            pyfalog.warning('GraphFrame handled event, however GraphFrame no longer exists. Ignoring event')
            return

        self.subplot.clear()
        self.subplot.grid(True)
        legend = []

        min_y = 0 if self.ctrlPanel.showY0 else None
        max_y = 0 if self.ctrlPanel.showY0 else None

        chosenX = self.ctrlPanel.xType
        chosenY = self.ctrlPanel.yType
        self.subplot.set(xlabel=self.ctrlPanel.formatLabel(chosenX), ylabel=self.ctrlPanel.formatLabel(chosenY))

        mainInput, miscInputs = self.ctrlPanel.getValues()
        view = self.getView()
        fits = self.ctrlPanel.fits
        if view.hasTargets:
            targets = self.ctrlPanel.targets
            iterList = tuple(itertools.product(fits, targets))
        else:
            iterList = tuple((f, None) for f in fits)
        for fit, target in iterList:
            try:
                xs, ys = view.getPlotPoints(mainInput, miscInputs, chosenX, chosenY, fit, target)

                # Figure out min and max Y
                min_y_this = min(ys, default=None)
                if min_y is None:
                    min_y = min_y_this
                elif min_y_this is not None:
                    min_y = min(min_y, min_y_this)
                max_y_this = max(ys, default=None)
                if max_y is None:
                    max_y = max_y_this
                elif max_y_this is not None:
                    max_y = max(max_y, max_y_this)

                self.subplot.plot(xs, ys)
                if target is None:
                    legend.append('{} ({})'.format(fit.name, fit.ship.item.getShortName()))
                else:
                    legend.append('{} ({}) vs {} ({})'.format(fit.name, fit.ship.item.getShortName(), target.name, target.ship.item.getShortName()))
            except Exception as ex:
                pyfalog.warning('Invalid values in "{0}"', fit.name)
                self.canvas.draw()
                self.Refresh()
                return

        # Special case for when we do not show Y = 0 and have no fits
        if min_y is None:
            min_y = 0
        if max_y is None:
            max_y = 0
        # Extend range a little for some visual space
        y_range = max_y - min_y
        min_y -= y_range * 0.05
        max_y += y_range * 0.05
        if min_y == max_y:
            min_y -= min_y * 0.05
            max_y += min_y * 0.05
        if min_y == max_y:
            min_y -= 5
            max_y += 5
        self.subplot.set_ylim(bottom=min_y, top=max_y)

        legend2 = []
        legend_colors = {
            0: 'blue',
            1: 'orange',
            2: 'green',
            3: 'red',
            4: 'purple',
            5: 'brown',
            6: 'pink',
            7: 'grey',
        }

        for i, i_name in enumerate(legend):
            try:
                selected_color = legend_colors[i]
            except:
                selected_color = None
            legend2.append(Patch(color=selected_color, label=i_name), )

        if len(legend2) > 0:
            leg = self.subplot.legend(handles=legend2)
            for t in leg.get_texts():
                t.set_fontsize('small')

            for l in leg.get_lines():
                l.set_linewidth(1)

        self.canvas.draw()
        self.Refresh()
