# =============================================================================
# Copyright (C) 2010 Diego Duclos, 2017 taleden
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

import bisect
import os
from logbook import Logger

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.targetResists import TargetResists as svc_TargetResists
import gui.display
import gui.mainFrame
import gui.globalEvents as GE
from gui.graph import Graph
from gui.bitmapLoader import BitmapLoader
import traceback
from gui.contextMenu import ContextMenu
from eos.saveddata.targetResists import TargetResists
import collections

pyfalog = Logger(__name__)

try:
    import matplotlib as mpl

    mpl_version = int(mpl.__version__[0]) or -1
    if mpl_version >= 2:
        mpl.use('wxagg')
        mplImported = True
    else:
        mplImported = False
    from matplotlib.patches import Patch
    from matplotlib.colors import hsv_to_rgb

    def hsl_to_hsv(hsl):  # why is this not in matplotlib.colors ?!
        h, s, l = hsl
        s *= l if (l < 0.5) else (1 - l)
        l += s
        return (h, 2 * s / l, l)

    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    from matplotlib.figure import Figure

    graphFrame_enabled = True
    mplImported = True
except ImportError as e:
    pyfalog.warning("Matplotlib failed to import.  Likely missing or incompatible version.")
    mpl_version = -1
    Patch = mpl = Canvas = Figure = None
    graphFrame_enabled = False
    mplImported = False
except Exception:
    # We can get exceptions deep within matplotlib. Catch those.  See GH #1046
    tb = traceback.format_exc()
    pyfalog.critical("Exception when importing Matplotlib. Continuing without importing.")
    pyfalog.critical(tb)
    mpl_version = -1
    Patch = mpl = Canvas = Figure = None
    graphFrame_enabled = False
    mplImported = False


class GraphFrame(wx.Frame):
    COLORS = (  # TODO find a good colorblind-friendly palette
        (   0 / 360.0, 1.0, 0.5 , "Red" ),
        ( 120 / 360.0, 1.0, 0.5 , "Green" ),
        ( 240 / 360.0, 1.0, 0.5 , "Blue" ),
        (  56 / 360.0, 1.0, 0.5 , "Yellow" ),
        ( 180 / 360.0, 1.0, 0.5 , "Cyan" ),
        ( 300 / 360.0, 1.0, 0.5 , "Magenta" ),
        (  40 / 360.0, 1.0, 0.5 , "Orange" ),
        ( 275 / 360.0, 1.0, 0.5 , "Purple" ),
        (   0 / 360.0, 0.7, 0.35, "Dark Red" ),
        ( 120 / 360.0, 0.7, 0.35, "Dark Green" ),
        ( 240 / 360.0, 0.7, 0.35, "Dark Blue" ),
        (  56 / 360.0, 0.7, 0.35, "Dark Yellow" ),
        ( 180 / 360.0, 0.7, 0.35, "Dark Cyan" ),
        ( 300 / 360.0, 0.7, 0.35, "Dark Magenta" ),
        (  40 / 360.0, 0.7, 0.35, "Dark Orange" ),
        ( 275 / 360.0, 0.7, 0.35, "Dark Purple" ),
        (   0 / 360.0, 0.7, 0.7 , "Light Red" ),
        ( 120 / 360.0, 0.7, 0.7 , "Light Green" ),
        ( 240 / 360.0, 0.7, 0.7 , "Light Blue" ),
        (  56 / 360.0, 0.7, 0.7 , "Light Yellow" ),
        ( 180 / 360.0, 0.7, 0.7 , "Light Cyan" ),
        ( 300 / 360.0, 0.7, 0.7 , "Light Magenta" ),
        (  40 / 360.0, 0.7, 0.7 , "Light Orange" ),
        ( 275 / 360.0, 0.7, 0.7 , "Light Purple" ),
    )

    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FRAME_FLOAT_ON_PARENT):
        wx.Frame.__init__(self, parent, title=u"pyfa: Graph Generator", style=style, size=(520, 390))

        try:
            self.plotPanel = PlotPanelMPL(self)
        except Exception as e:
            pyfalog.critical(e)
            return

        self.SetIcon(wx.IconFromBitmap(BitmapLoader.getBitmap("graphs_small", "gui")))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.CreateStatusBar()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.graphSelection = wx.Choice(self)
        for view in Graph.views:
            view = view()
            self.graphSelection.Append(view.getName(), view)
        sizer.Add(self.graphSelection, 0, wx.EXPAND)

        sizer.Add(self.plotPanel, 1, wx.EXPAND)

        linePanel = wx.Panel(self)
        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        linePanel.SetSizer(lineSizer)
        sizer.Add(linePanel, 0, wx.EXPAND)

        self.buttonLineColor = wx.Button(linePanel, label=" ", style=wx.BU_EXACTFIT | wx.BORDER_NONE)
        self.buttonLineColor.SetSize(2 * self.buttonLineColor.GetSize()[-1:])
        lineSizer.Add(self.buttonLineColor, 0, flag=wx.SHAPED | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)

        self.labelLine = wx.StaticText(linePanel, label="")
        lineSizer.Add(self.labelLine, 1, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)

        sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)

        self.controlPanel = wx.Panel(self)
        self.controlSizer = wx.BoxSizer(wx.VERTICAL)
        self.controlPanel.SetSizer(self.controlSizer)
        sizer.Add(self.controlPanel, 0, wx.EXPAND)

        sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), 0, wx.EXPAND)

        listPanel = wx.Panel(self)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        listPanel.SetSizer(listSizer)
        sizer.Add(listPanel, 0, wx.EXPAND)

        self.fitList = FitList(listPanel, self)
        self.fitList.SetMinSize((270, -1))
        listSizer.Add(self.fitList, 1, wx.EXPAND)

        self.tgtList = TargetList(listPanel, self)
        self.tgtList.SetMinSize((270, -1))
        listSizer.Add(self.tgtList, 1, wx.EXPAND)

        self.graphSelection.Bind(wx.EVT_CHOICE, self.onSelectViewChanged)
        self.buttonLineColor.Bind(wx.EVT_BUTTON, self.onButtonColorClick)
        self.Bind(EVT_COLORPOPUP_SELECT, self.onSelectColor)
        self.fitList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.fitList.fitList.Bind(wx.EVT_RIGHT_DOWN, self.onAttackerContext)
        self.tgtList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.removeTarget)
        self.tgtList.fitList.Bind(wx.EVT_RIGHT_DOWN, self.onTargetContext)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.onFitChanged)
        self.mainFrame.Bind(GE.TARGET_RESISTS_CHANGED, self.onTargetResistsChanged)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.dummyTargetProfile = TargetResists()
        self.dummyTargetProfile.name = "Dummy"
        self.fits = collections.OrderedDict()
        fitID = self.mainFrame.getActiveFit()
        if fitID:
            self.fits[fitID] = Fit.getInstance().getFit(fitID)
        self.fitList.fitList.update(self.fits.values())
        self.tgts = collections.OrderedDict()
        self.fields = {}
        self.markerX = 0
        self.selected = None
        self.nextColor = 0
        self.lineColor = {}
        self.lineData = {}
        self.currentViewIndex = None
        self.currentView = None
        self.selectView(0)
        self.Fit()
        self.SetMinSize(self.GetSize())

    def onClose(self, event):
        self.graphSelection.Unbind(wx.EVT_CHOICE, handler=self.onSelectViewChanged)
        self.buttonLineColor.Unbind(wx.EVT_BUTTON, handler=self.onButtonColorClick)
        self.Unbind(EVT_COLORPOPUP_SELECT, handler=self.onSelectColor)
        self.fitList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.removeItem)
        self.fitList.fitList.Unbind(wx.EVT_RIGHT_DOWN, handler=self.onAttackerContext)
        self.tgtList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.removeTarget)
        self.tgtList.fitList.Unbind(wx.EVT_RIGHT_DOWN, handler=self.onTargetContext)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.onFitChanged)
        self.mainFrame.Unbind(GE.TARGET_RESISTS_CHANGED, handler=self.onTargetResistsChanged)
        event.Skip()

    def onSelectViewChanged(self, event):
        self.selectView(self.graphSelection.GetSelection())

    def selectView(self, index):
        if self.currentViewIndex == index:
            return
        self.currentViewIndex = index
        self.currentView = self.graphSelection.GetClientData(index)
        self.graphSelection.SetSelection(index)

        self.controlPanel.DestroyChildren()
        self.fields.clear()

        viewPanel = self.currentView.getControlPanel(self.controlPanel, self.onFieldChanged)
        if not viewPanel:
            fields = self.currentView.getFields()
            if fields:
                viewPanel = wx.Panel(self.controlPanel)
                viewSizer = wx.FlexGridSizer(0, 4)
                viewSizer.AddGrowableCol(1)
                viewPanel.SetSizer(viewSizer)

                # Setup textboxes
                icons = self.currentView.getIcons()
                labels = self.currentView.getLabels()
                for field in sorted(fields.keys()):
                    textBox = wx.TextCtrl(viewPanel)
                    self.fields[field] = textBox
                    textBox.Bind(wx.EVT_TEXT_ENTER, self.onFieldChanged)
                    textBox.Bind(wx.EVT_KILL_FOCUS, self.onFieldChanged)
                    defaultVal = fields[field]
                    if defaultVal is not None:
                        if not isinstance(defaultVal, basestring):
                            defaultVal = "%g" % (defaultVal,)
                        textBox.ChangeValue(defaultVal)
                    viewSizer.Add(textBox, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)

                    imgLabelSizer = wx.BoxSizer(wx.HORIZONTAL)

                    icon = icons.get(field) if icons else None
                    if icon is not None:
                        static = wx.StaticBitmap(viewPanel, bitmap=icon)
                        imgLabelSizer.Add(static, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=1)

                    label = labels.get(field, field) if labels else field
                    imgLabelSizer.Add(wx.StaticText(viewPanel, label=label), proportion=0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, border=3)

                    viewSizer.Add(imgLabelSizer, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL)

        if viewPanel is not None:
            self.controlSizer.Add(viewPanel, 0, wx.EXPAND)

        self.tgts.clear()
        if self.currentView.allowTargetResists():
            for fitID, fit in self.fits.iteritems():
                tgtID = fit.targetResists.name if fit.targetResists else ""
                if tgtID not in self.tgts:
                    self.tgts[tgtID] = svc_TargetResists.getTargetResists(tgtID) if tgtID else self.dummyTargetProfile
            self.tgtList.Show()
        elif self.currentView.allowTargetFits():
            self.tgtList.Show()
        else:
            self.tgtList.Hide()
        self.tgtList.fitList.update(self.tgts.values())

        self.nextColor = 0
        self.markerX = 0
        self.selected = None

        self.Layout()
        self.calculate()
        self.draw()

    def getValues(self):
        values = {}
        for fieldName, field in self.fields.iteritems():
            values[fieldName] = field.GetValue()

        return values

    def AppendFitToList(self, fitID, fit=None):
        if fitID not in self.fits:
            self.fits[fitID] = fit or Fit.getInstance().getFit(fitID)
            self.fitList.fitList.update(self.fits.values())
            self.calculate(fitID)
            self.draw()

    def addTargetFit(self, fitID, fit=None):
        if self.currentView.allowTargetFits() and (fitID not in self.tgts):
            self.tgts[fitID] = fit or Fit.getInstance().getFit(fitID)
            self.tgtList.fitList.update(self.tgts.values())
            self.calculate(fitID)
            self.draw()

    def addTargetProfile(self, profile):
        tgtID = profile.name if profile else ""
        if self.currentView.allowTargetResists() and (tgtID not in self.tgts):
            self.tgts[tgtID] = profile or self.dummyTargetProfile
            self.tgtList.fitList.update(self.tgts.values())
            self.calculate(tgtID)
            self.draw()

    def removeItem(self, event):
        row, _ = self.fitList.fitList.HitTest(event.Position)
        if row != -1:
            fitID = list(self.fits.keys())[row]
            del self.fits[fitID]
            self.fitList.fitList.update(self.fits.values())
            trash = list(lineID for lineID in self.lineData if lineID[0] == fitID)
            for lineID in trash:
                del self.lineData[lineID]
            if self.selected in trash:
                self.selected = None
            self.draw()

    def removeTarget(self, event):
        row, _ = self.tgtList.fitList.HitTest(event.Position)
        if row != -1:
            tgtID = list(self.tgts.keys())[row]
            del self.tgts[tgtID]
            self.tgtList.fitList.update(self.tgts.values())
            trash = list(lineID for lineID in self.lineData if lineID[1] == tgtID)
            for lineID in trash:
                del self.lineData[lineID]
            if self.selected in trash:
                self.selected = None
            self.draw()

    def onAttackerContext(self, event):
        menu = ContextMenu.getMenu(None, ("graphAttacker",))
        if menu is not None:
            self.fitList.fitList.PopupMenu(menu)

    def onTargetContext(self, event):
        if self.currentView.allowTargetFits() and self.currentView.allowTargetResists():
            context = "graphTargetFitsResists"
        elif self.currentView.allowTargetFits():
            context = "graphTargetFits"
        elif self.currentView.allowTargetResists():
            context = "graphTargetResists"
        else:
            return
        menu = ContextMenu.getMenu(None, (context,))
        if menu is not None:
            self.tgtList.fitList.PopupMenu(menu)

    def onFitChanged(self, event):
        update = False
        if event.fitID in self.fits:
            self.fitList.fitList.update(self.fits.values())
            update = True
        if event.fitID in self.tgts:
            self.tgtList.fitList.update(self.tgts.values())
            update = True
        if update:
            self.calculate(event.fitID)
            self.draw()
        event.Skip()

    def onTargetResistsChanged(self, event):
        if event.name in self.tgts:
            self.tgtList.fitList.update(self.tgts.values())
            self.calculate(event.name)
            self.draw()
        event.Skip()

    def onFieldChanged(self, event=None):
        self.calculate()
        self.draw()
        if event:
            event.Skip()

    def setMarkerX(self, markerX):
        self.markerX = markerX
        self.calculate(markerOnly=True)
        self.draw()

    def setSelectedLine(self, lineID):
        self.selected = lineID if (lineID in self.lineData) else None
        self.draw()

    def onButtonColorClick(self, event):
        if self.selected:
            win = ColorPickerPopup(self, self.COLORS, 8, 3)
            pos = wx.GetMousePosition()
            win.Position(pos, (0, 0))
            win.Popup()

    def onSelectColor(self, event):
        if self.selected in self.lineData:
            self.lineColor[self.selected] = tuple(c / 255.0 for c in event.color.Get(False))
            self.draw()

    def calculate(self, calcID=None, markerOnly=False):
        values = self.getValues()
        sFit = Fit.getInstance()
        oldLineData = self.lineData
        self.lineData = {}
        # don't clear lineColor so that removing and re-adding a pairing re-uses the previous color

        for fitID, fit in self.fits.iteritems():
            for tgtID, tgt in (self.tgts.iteritems() if self.tgts else ((None, None),)):
                lineID = (fitID, tgtID)

                # if we're only recalculating for a specific fit, recycle plotted data for lines that don't involve that fit
                if (lineID in oldLineData) and (calcID is not None):
                    if ((type(calcID) != type(fitID)) or (calcID != fitID)) and ((type(calcID) != type(tgtID)) or (calcID != tgtID)):
                        self.lineData[lineID] = oldLineData[lineID]
                        continue

                color = self.lineColor.get(lineID)
                if color is None:
                    color = hsv_to_rgb(hsl_to_hsv(self.COLORS[self.nextColor][:3]))
                    self.nextColor = (self.nextColor + 1) % len(self.COLORS)
                    self.lineColor[lineID] = color
                if tgtID is None:
                    tgt = None
                elif tgtID == "":
                    tgt = self.dummyTargetProfile
                elif type(tgtID) is int:
                    tgt = sFit.getFit(tgtID)
                else:
                    tgt = svc_TargetResists.getTargetResists(tgtID)

                try:
                    if markerOnly and (lineID in oldLineData):
                        self.lineData[lineID] = oldLineData[lineID]
                    else:
                        x_success, y_status = self.currentView.getPoints(values, fit, tgt)
                        if not x_success:
                            # TODO: Add a pwetty statys bar to report errors with
                            self.SetStatusText(y_status)
                            return False
                        self.lineData[lineID] = [x_success, y_status, None]

                    markerY = self.currentView.getPoint(values, (self.markerX,), fit, tgt) if self.markerX else None
                    if self.markerX and markerY is None:
                        x = bisect.bisect(self.lineData[lineID][0], self.markerX)
                        if x > 0 and x < (len(self.lineData[lineID][1]) - 1):
                            dx = (self.lineData[lineID][0][x] - self.lineData[lineID][0][x - 1])
                            dy = (self.lineData[lineID][1][x] - self.lineData[lineID][1][x - 1])
                            markerY = self.lineData[lineID][1][x - 1] + dy * (self.markerX - self.lineData[lineID][0][x - 1]) / dx
                    self.lineData[lineID][2] = markerY

                except ValueError as e:
                    msg = u"Error calculating fit '{}' vs target '{}'".format(fit.name, (tgt.name if tgt else "N/A"))
                    self.SetStatusText(msg)
                    pyfalog.warning(msg)
                    pyfalog.warning(str(e))
                    return False
            # for tgtID
        # for fitID

        self.plotPanel.labelX.SetLabel(self.currentView.getVariableLabels(values)[0])
        self.SetStatusText("")
        return True
    # calculate()

    def draw(self):
        lineDataGen = (([lineID] + lineXYM + [self.lineColor.get(lineID), lineID == self.selected]) for lineID, lineXYM in self.lineData.iteritems())
        self.plotPanel.draw(lineDataGen, self.markerX)
        if self.selected:
            self.buttonLineColor.Enable()
            self.buttonLineColor.SetBackgroundColour(tuple(c * 255 for c in self.lineColor[self.selected]))
            fitID, tgtID = self.selected
            if tgtID is None:
                self.labelLine.SetLabel(self.fits[fitID].name)
            else:
                self.labelLine.SetLabel("%s vs. %s" % (self.fits[fitID].name, self.tgts[tgtID].name))
        else:
            self.buttonLineColor.Disable()
            self.buttonLineColor.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
            self.labelLine.SetLabel("")


class FitList(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)
        self.frame = frame

        self.fitList = FitDisplay(self)
        self.mainSizer.Add(self.fitList, 1, wx.EXPAND)
        fitToolTip = wx.ToolTip("Right-click or drag to add an attacker fit; double-click to remove")
        self.fitList.SetToolTip(fitToolTip)

    def handleDrag(self, type, fitID):
        if type == "fit":
            self.frame.AppendFitToList(fitID)


class FitDisplay(gui.display.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name:Attacker Name"]

    def __init__(self, parent):
        gui.display.Display.__init__(self, parent)


class TargetList(wx.Panel):
    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)
        self.frame = frame

        self.fitList = TargetDisplay(self)
        self.mainSizer.Add(self.fitList, 1, wx.EXPAND)
        fitToolTip = wx.ToolTip("Right-click or drag to add a target fit or profile; double-click to remove")
        self.fitList.SetToolTip(fitToolTip)

    def handleDrag(self, type, fitID):
        if type == "fit":
            self.frame.addTargetFit(fitID)


class TargetDisplay(gui.display.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name:Target Name"]

    def __init__(self, parent):
        gui.display.Display.__init__(self, parent)


class PlotPanelMPL(wx.Panel):
    def __init__(self, parent):
        global graphFrame_enabled
        global mplImported
        global mpl_version

        if not graphFrame_enabled:
            pyfalog.warning("Matplotlib is not enabled. Skipping initialization.")
            raise Exception()

        try:
            cache_dir = mpl._get_cachedir()
        except:
            cache_dir = os.path.expanduser(os.path.join("~", ".matplotlib"))
        cache_file = os.path.join(cache_dir, 'fontList.cache')
        if os.access(cache_dir, os.W_OK | os.X_OK) and os.path.isfile(cache_file):
            # remove matplotlib font cache, see #234
            os.remove(cache_file)
        if not mplImported:
            mpl.use('wxagg')

        graphFrame_enabled = True
        self.legendFix = False
        if int(mpl.__version__[0]) < 1:
            print("pyfa: Found matplotlib version ", mpl.__version__, " - activating OVER9000 workarounds")
            print("pyfa: Recommended minimum matplotlib version is 1.0.0")
            self.legendFix = True
        mplImported = True

        wx.Panel.__init__(self, parent)

        self.sizer = wx.FlexGridSizer(2, 2)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(1)
        self.SetSizer(self.sizer)

        self.labelY = wx.StaticText(self, label="")  # TODO custom control for rotated text?
        self.sizer.Add(self.labelY, flag=wx.ALIGN_CENTER | wx.ALL, border=3)

        self.figure = Figure(figsize=(4, 3))
        colorByte = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        colorFloat = [c / 255. for c in colorByte]
        self.figure.set_facecolor(colorFloat)
        self.figure.set_edgecolor(colorFloat)
        self.subplot = self.figure.add_axes([0, 0, 1, 1])

        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(*colorByte))
        self.canvas.mpl_connect('pick_event', lambda event: self.onPick(event))
        self.canvas.mpl_connect('button_press_event', lambda event: self.onPlotClick(event))
        self.sizer.Add(self.canvas, proportion=1, flag=wx.EXPAND)

        self.sizer.Add(wx.StaticText(self, label=""), flag=wx.ALIGN_CENTER | wx.ALL, border=3)

        self.labelX = wx.StaticText(self, label="")
        self.sizer.Add(self.labelX, flag=wx.ALIGN_CENTER | wx.ALL, border=3)

        self._parent = parent
        self._lines = {}
        self.ondrag = None
        self.onrelease = None

    def draw(self, lineData, markerX=None):
        self._lines.clear()
        self.maxX = 1
        self.maxY = 1
        self.subplot.clear()
        self.subplot.grid(True)

        for lineID, xdata, ydata, markerY, color, selected in lineData:
            self._lines[lineID], = self.subplot.plot(xdata, ydata, color=color, linewidth=(2 if selected else 1), picker=5)
            self.maxX = max(self.maxX, max(xdata))
            self.maxY = max(self.maxY, max(ydata))
            if markerX and (markerY is not None):
                self.subplot.annotate(
                    "%.1f" % (markerY,),
                    xy=(markerX, markerY), xytext=(-1, 1), textcoords="offset pixels",
                    ha="right", va="bottom", fontsize="small"
                )
        if markerX:
            self.subplot.axvline(x=markerX, linestyle="dotted", linewidth=1, color=(0, 0, 0))
            self.subplot.annotate(
                "@ %.1f" % (markerX,),
                xy=(markerX, self.maxY * 1.1), xytext=(-1, -1), textcoords="offset pixels",
                ha="right", va="top", fontsize="small"
            )

        self.subplot.set_xlim(left=0, right=self.maxX * 1.05)
        self.subplot.set_ylim(bottom=0, top=self.maxY * 1.1)
        self.subplot.tick_params(direction="in", width=2, length=6)

        self.subplot.tick_params(axis="x", pad=-5.0)
        tickvalues = mpl.ticker.MaxNLocator(nbins=15, steps=[1, 2, 5, 10], integer=True, min_n_ticks=10, prune="lower").tick_values(0, self.maxX * 1.025)
        xticks = list(int(v) for v in tickvalues)
        self.subplot.set_xticks(xticks)
        self.subplot.set_xticklabels(xticks, va="bottom")

        self.subplot.tick_params(axis="y", pad=-8.0)
        tickvalues = mpl.ticker.MaxNLocator(nbins=12, steps=[1, 2, 5, 10], integer=True, min_n_ticks=8, prune="lower").tick_values(0, self.maxY * 1.05)
        yticks = list(int(v) for v in tickvalues)
        self.subplot.set_yticks(yticks)
        self.subplot.set_yticklabels(yticks, ha="left")

        self.canvas.draw()

    def onPlotClick(self, event):
        if event.button == 3:
            self._parent.setMarkerX(event.xdata)
            if not self.ondrag:
                self.ondrag = self.canvas.mpl_connect('motion_notify_event', lambda event: self.onPlotDrag(event))
            if not self.onrelease:
                self.onrelease = self.canvas.mpl_connect('button_release_event', lambda event: self.onPlotRelease(event))

    def onPlotDrag(self, event):
        self._parent.setMarkerX(event.xdata)

    def onPlotRelease(self, event):
        if event.button == 3:
            self._parent.setMarkerX(event.xdata)
            if self.ondrag:
                self.canvas.mpl_disconnect(self.ondrag)
                self.ondrag = None
            if self.onrelease:
                self.canvas.mpl_disconnect(self.onrelease)
                self.onrelease = None

    def onPick(self, event):
        for lineID, line in self._lines.iteritems():
            if line == event.artist:
                self._parent.setSelectedLine(lineID)
# PlotPanelMPL


COLORPOPUP_SELECT = wx.NewEventType()
EVT_COLORPOPUP_SELECT = wx.PyEventBinder(COLORPOPUP_SELECT, 0)


class ColorPopupSelectEvent(wx.PyCommandEvent):
    def __init__(self, windowID, color):
        wx.PyCommandEvent.__init__(self, COLORPOPUP_SELECT, windowID)
        self.color = color
    # __init__()
# ColorPopupSelectEvent


class ColorPickerPopup(wx.PopupTransientWindow):

    def __init__(self, parent, colors, ncol=0, nrow=0):
        wx.PopupTransientWindow.__init__(self, parent, style=wx.BORDER_SIMPLE)
        self.parent = parent
        ncol = ncol or len(colors)
        nrow = nrow or int(len(colors) / ncol) + (1 if (len(colors) % ncol) else 0)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        grid = wx.GridSizer(nrow, ncol, 0, 0)
        self.patches = list()
        for hsln in colors:
            patch = wx.StaticText(self, label=wx.EmptyString, size=wx.Size(24, 24), style=wx.BORDER_STATIC)
            color = wx.Colour(*(v*255 for v in hsv_to_rgb(hsl_to_hsv(hsln[:3]))))
            patch.SetBackgroundColour(color)
            patch.SetToolTipString(hsln[3])
            patch.Bind(wx.EVT_LEFT_UP, self.OnLeftUp_Patch)
            grid.Add(patch, flag=wx.ALL, border=3)
        sizer.Add(grid)

        line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        sizer.Add(line, flag=wx.EXPAND)

        button = wx.Button(self, label="Custom")
        button.SetToolTipString("Choose a custom color")
        button.Bind(wx.EVT_BUTTON, self.OnButton_Custom)
        sizer.Add(button, flag=wx.EXPAND | wx.ALL, border=2)

        sizer.Fit(self)
        self.Layout()
    # __init__()

    def OnLeftUp_Patch(self, evt):
        self.PickColor(evt.GetEventObject().GetBackgroundColour())
    # OnLeftUp_Patch()

    def OnButton_Custom(self, evt):
        data = wx.ColourData()
        data.SetChooseFull(True)
        dialog = wx.ColourDialog(self.parent, data)
        if dialog.ShowModal() == wx.ID_OK:
            self.PickColor(dialog.GetColourData().Colour)
        dialog.Destroy()
    # OnButton_Custom()

    def PickColor(self, color):
        evt = ColorPopupSelectEvent(self.parent.GetId(), color)
        self.parent.GetEventHandler().AddPendingEvent(evt)
        self.Hide()
        self.Destroy()
    # PickColor()

# ColorPickerPopup
