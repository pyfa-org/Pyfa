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


import os
import traceback

# noinspection PyPackageRequirements
import wx
from logbook import Logger

import gui.display
import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.builtinGraphs.base import Graph
from service.fit import Fit
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

        try:
            cache_dir = mpl._get_cachedir()
        except:
            cache_dir = os.path.expanduser(os.path.join('~', '.matplotlib'))

        cache_file = os.path.join(cache_dir, 'fontList.cache')

        if os.access(cache_dir, os.W_OK | os.X_OK) and os.path.isfile(cache_file):
            # remove matplotlib font cache, see #234
            os.remove(cache_file)

        wx.Frame.__init__(self, parent, title='pyfa: Graph Generator', style=style, size=(520, 390))

        i = wx.Icon(BitmapLoader.getBitmap('graphs_small', 'gui'))
        self.SetIcon(i)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.CreateStatusBar()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.mainSizer.Add(self.graphSelection, 0, wx.EXPAND)
        self.selectedYRbMap = {}

        self.figure = Figure(figsize=(5, 3), tight_layout={'pad': 1.08})

        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        clr = [c / 255. for c in rgbtuple]
        self.figure.set_facecolor(clr)
        self.figure.set_edgecolor(clr)

        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))

        self.subplot = self.figure.add_subplot(111)
        self.subplot.grid(True)

        self.mainSizer.Add(self.canvas, 1, wx.EXPAND)
        self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0,
                           wx.EXPAND)


        self.ctrlPanel = GraphControlPanel(self, self)
        self.mainSizer.Add(self.ctrlPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.drawTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.draw, self.drawTimer)

        for view in Graph.views:
            view = view()
            self.graphSelection.Append(view.name, view)

        self.graphSelection.SetSelection(0)
        self.fields = {}
        self.updateGraphWidgets()
        self.sl1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.mainSizer.Add(self.sl1, 0, wx.EXPAND)


        self.ctrlPanel.fitList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.ctrlPanel.fitList.fitList.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.ctrlPanel.showY0Cb.Bind(wx.EVT_CHECKBOX, self.OnNonDestructiveControlsUpdate)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.OnFitChanged)
        self.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)
        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.Bind(wx.EVT_CHOICE, self.graphChanged)
        from gui.builtinStatsViews.resistancesViewFull import EFFECTIVE_HP_TOGGLED  # Grr crclar gons
        self.mainFrame.Bind(EFFECTIVE_HP_TOGGLED, self.OnEhpToggled)

        self.contextMenu = wx.Menu()
        removeItem = wx.MenuItem(self.contextMenu, 1, 'Remove Fit')
        self.contextMenu.Append(removeItem)
        self.contextMenu.Bind(wx.EVT_MENU, self.ContextMenuHandler, removeItem)

        self.Fit()
        self.SetMinSize(self.GetSize())

    def handleDrag(self, type, fitID):
        if type == 'fit':
            self.AppendFitToList(fitID)

    def closeEvent(self, event):
        self.closeWindow()
        event.Skip()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == wx.WXK_ESCAPE and mstate.GetModifiers() == wx.MOD_NONE:
            self.closeWindow()
            return
        elif keycode == 65 and mstate.GetModifiers() == wx.MOD_CONTROL:
            self.ctrlPanel.fitList.fitList.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and mstate.GetModifiers() == wx.MOD_NONE:
            self.removeFits(self.getSelectedFits())
        event.Skip()

    def OnContextMenu(self, event):
        if self.getSelectedFits():
            self.PopupMenu(self.contextMenu)

    def ContextMenuHandler(self, event):
        selectedMenuItem = event.GetId()
        if selectedMenuItem == 1:  # Copy was chosen
            fits = self.getSelectedFits()
            self.removeFits(fits)

    def OnEhpToggled(self, event):
        event.Skip()
        view = self.getView()
        if view.redrawOnEffectiveChange:
            view.clearCache()
            self.draw()

    def OnFitChanged(self, event):
        event.Skip()
        view = self.getView()
        view.clearCache(key=event.fitID)
        self.draw()

    def OnFitRemoved(self, event):
        event.Skip()
        fit = next((f for f in self.ctrlPanel.fits if f.ID == event.fitID), None)
        if fit is not None:
            self.removeFits([fit])

    def graphChanged(self, event):
        self.ctrlPanel.selectedY = None
        self.updateGraphWidgets()
        event.Skip()

    def closeWindow(self):
        from gui.builtinStatsViews.resistancesViewFull import EFFECTIVE_HP_TOGGLED  # Grr gons
        self.ctrlPanel.fitList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.OnLeftDClick)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.OnFitChanged)
        self.mainFrame.Unbind(GE.FIT_REMOVED, handler=self.OnFitRemoved)
        self.mainFrame.Unbind(EFFECTIVE_HP_TOGGLED, handler=self.OnEhpToggled)
        self.Destroy()

    def getView(self):
        return self.graphSelection.GetClientData(self.graphSelection.GetSelection())

    def getValues(self):
        values = {}
        for fieldHandle, field in self.fields.items():
            values[fieldHandle] = field.GetValue()

        return values

    def OnNonDestructiveControlsUpdate(self, event):
        event.Skip()
        self.draw()

    def OnYTypeUpdate(self, event):
        event.Skip()
        obj = event.GetEventObject()
        formatName = obj.GetLabel()
        self.ctrlPanel.selectedY = self.selectedYRbMap[formatName]
        self.draw()

    def updateGraphWidgets(self):
        view = self.getView()
        view.clearCache()
        self.ctrlPanel.graphSubselSizer.Clear()
        self.ctrlPanel.inputsSizer.Clear()
        for child in self.ctrlPanel.Children:
            if child not in (self.ctrlPanel.showY0Cb, self.ctrlPanel.fitList, self.ctrlPanel.targetList):
                child.Destroy()
        self.fields.clear()

        # Setup view options
        self.selectedYRbMap.clear()
        if len(view.yDefs) > 1:
            i = 0
            for yAlias, yDef in view.yDefs.items():
                if i == 0:
                    rdo = wx.RadioButton(self.ctrlPanel, wx.ID_ANY, yDef.switchLabel, style=wx.RB_GROUP)
                else:
                    rdo = wx.RadioButton(self.ctrlPanel, wx.ID_ANY, yDef.switchLabel)
                rdo.Bind(wx.EVT_RADIOBUTTON, self.OnYTypeUpdate)
                if i == (self.ctrlPanel.selectedY or 0):
                    rdo.SetValue(True)
                self.ctrlPanel.graphSubselSizer.Add(rdo, 0, wx.ALL | wx.EXPAND, 0)
                self.selectedYRbMap[yDef.switchLabel] = i
                i += 1

        # Setup inputs
        for fieldHandle, fieldDef in (('x', view.xDef), *view.extraInputs.items()):
            textBox = wx.TextCtrl(self.ctrlPanel, wx.ID_ANY, style=0)
            self.fields[fieldHandle] = textBox
            textBox.Bind(wx.EVT_TEXT, self.onFieldChanged)
            self.ctrlPanel.inputsSizer.Add(textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            if fieldDef.inputDefault is not None:
                inputDefault = fieldDef.inputDefault
                if not isinstance(inputDefault, str):
                    inputDefault = ('%f' % inputDefault).rstrip('0')
                    if inputDefault[-1:] == '.':
                        inputDefault += '0'

                textBox.ChangeValue(inputDefault)

            imgLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
            if fieldDef.inputIconID:
                icon = BitmapLoader.getBitmap(fieldDef.inputIconID, 'icons')
                if icon is not None:
                    static = wx.StaticBitmap(self.ctrlPanel)
                    static.SetBitmap(icon)
                    imgLabelSizer.Add(static, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)

            imgLabelSizer.Add(wx.StaticText(self.ctrlPanel, wx.ID_ANY, fieldDef.inputLabel), 0,
                              wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.ctrlPanel.inputsSizer.Add(imgLabelSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.Layout()
        self.draw()

    def delayedDraw(self, event=None):
        self.drawTimer.Stop()
        self.drawTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def draw(self, event=None):
        global mpl_version

        if event is not None:
            event.Skip()

        self.drawTimer.Stop()

        # todo: FIX THIS, see #1430. draw() is not being unbound properly when the window closes, this is an easy fix,
        # but not a proper solution
        if not self:
            pyfalog.warning('GraphFrame handled event, however GraphFrame no longer exists. Ignoring event')
            return

        values = self.getValues()
        view = self.getView()
        self.subplot.clear()
        self.subplot.grid(True)
        legend = []

        min_y = 0 if self.ctrlPanel.showY0 else None
        max_y = 0 if self.ctrlPanel.showY0 else None

        xRange = values['x']
        extraInputs = {ih: values[ih] for ih in view.extraInputs}
        try:
            chosenY = [i for i in view.yDefs.keys()][self.ctrlPanel.selectedY or 0]
        except IndexError:
            chosenY = [i for i in view.yDefs.keys()][0]

        self.subplot.set(xlabel=view.xDef.axisLabel, ylabel=view.yDefs[chosenY].axisLabel)

        for fit in self.ctrlPanel.fits:
            try:
                xs, ys = view.getPlotPoints(fit, extraInputs, xRange, 100, chosenY)

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
                legend.append('{} ({})'.format(fit.name, fit.ship.item.getShortName()))
            except Exception as ex:
                pyfalog.warning('Invalid values in "{0}"', fit.name)
                self.SetStatusText('Invalid values in "%s"' % fit.name)
                self.canvas.draw()
                return

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
        self.SetStatusText('')
        self.Refresh()

    def onFieldChanged(self, event):
        view = self.getView()
        view.clearCache()
        self.delayedDraw()

    def AppendFitToList(self, fitID):
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit not in self.ctrlPanel.fits:
            self.ctrlPanel.fits.append(fit)

        self.ctrlPanel.fitList.fitList.update(self.ctrlPanel.fits)
        self.draw()

    def OnLeftDClick(self, event):
        row, _ = self.ctrlPanel.fitList.fitList.HitTest(event.Position)
        if row != -1:
            try:
                fit = self.ctrlPanel.fits[row]
            except IndexError:
                pass
            else:
                self.removeFits([fit])

    def removeFits(self, fits):
        toRemove = [f for f in fits if f in self.ctrlPanel.fits]
        if not toRemove:
            return
        for fit in toRemove:
            self.ctrlPanel.fits.remove(fit)
        self.ctrlPanel.fitList.fitList.update(self.ctrlPanel.fits)
        view = self.getView()
        for fit in fits:
            view.clearCache(key=fit.ID)
        self.draw()

    def getSelectedFits(self):
        fits = []
        for row in self.ctrlPanel.fitList.fitList.getSelectedRows():
            try:
                fit = self.ctrlPanel.fits[row]
            except IndexError:
                continue
            fits.append(fit)
        return fits
