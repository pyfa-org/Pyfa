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
from logbook import Logger

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
import gui.display
import gui.mainFrame
import gui.globalEvents as GE
from gui.graph import Graph
from gui.bitmapLoader import BitmapLoader
import traceback

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
    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FRAME_FLOAT_ON_PARENT):
        global graphFrame_enabled
        global mplImported
        global mpl_version

        self.legendFix = False

        if not graphFrame_enabled:
            pyfalog.warning("Matplotlib is not enabled. Skipping initialization.")
            return

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
        if int(mpl.__version__[0]) < 1:
            print("pyfa: Found matplotlib version ", mpl.__version__, " - activating OVER9000 workarounds")
            print("pyfa: Recommended minimum matplotlib version is 1.0.0")
            self.legendFix = True

        mplImported = True

        wx.Frame.__init__(self, parent, title=u"pyfa: Graph Generator", style=style, size=(520, 390))

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        self.SetIcon(i)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.CreateStatusBar()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())
        self.fits = [fit] if fit is not None else []
        self.fitList = FitList(self)
        self.fitList.SetMinSize((270, -1))

        self.fitList.fitList.update(self.fits)

        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.mainSizer.Add(self.graphSelection, 0, wx.EXPAND)

        self.figure = Figure(figsize=(4, 3))

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

        self.gridPanel = wx.Panel(self)
        self.mainSizer.Add(self.gridPanel, 0, wx.EXPAND)

        dummyBox = wx.BoxSizer(wx.VERTICAL)
        self.gridPanel.SetSizer(dummyBox)

        self.gridSizer = wx.FlexGridSizer(0, 4)
        self.gridSizer.AddGrowableCol(1)
        dummyBox.Add(self.gridSizer, 0, wx.EXPAND)

        for view in Graph.views:
            view = view()
            self.graphSelection.Append(view.name, view)

        self.graphSelection.SetSelection(0)
        self.fields = {}
        self.select(0)
        self.sl1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.mainSizer.Add(self.sl1, 0, wx.EXPAND)
        self.mainSizer.Add(self.fitList, 0, wx.EXPAND)

        self.fitList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.draw)
        self.Bind(wx.EVT_CLOSE, self.close)

        self.Fit()
        self.SetMinSize(self.GetSize())

    def handleDrag(self, type, fitID):
        if type == "fit":
            self.AppendFitToList(fitID)

    def close(self, event):
        self.fitList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.removeItem)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.draw)
        event.Skip()

    def getView(self):
        return self.graphSelection.GetClientData(self.graphSelection.GetSelection())

    def getValues(self):
        values = {}
        for fieldName, field in self.fields.iteritems():
            values[fieldName] = field.GetValue()

        return values

    def select(self, index):
        view = self.getView()
        icons = view.getIcons()
        labels = view.getLabels()
        sizer = self.gridSizer
        self.gridPanel.DestroyChildren()
        self.fields.clear()

        # Setup textboxes
        for field, defaultVal in view.getFields().iteritems():

            textBox = wx.TextCtrl(self.gridPanel, wx.ID_ANY, style=0)
            self.fields[field] = textBox
            textBox.Bind(wx.EVT_TEXT, self.onFieldChanged)
            sizer.Add(textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            if defaultVal is not None:
                if not isinstance(defaultVal, basestring):
                    defaultVal = ("%f" % defaultVal).rstrip("0")
                    if defaultVal[-1:] == ".":
                        defaultVal += "0"

                textBox.ChangeValue(defaultVal)

            imgLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
            if icons:
                icon = icons.get(field)
                if icon is not None:
                    static = wx.StaticBitmap(self.gridPanel)
                    static.SetBitmap(icon)
                    imgLabelSizer.Add(static, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)

            if labels:
                label = labels.get(field)
                label = label if label is not None else field
            else:
                label = field

            imgLabelSizer.Add(wx.StaticText(self.gridPanel, wx.ID_ANY, label), 0,
                              wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
            sizer.Add(imgLabelSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.draw()

    def draw(self, event=None):
        global mpl_version

        values = self.getValues()
        view = self.getView()
        self.subplot.clear()
        self.subplot.grid(True)
        legend = []

        for fit in self.fits:
            try:
                success, status = view.getPoints(fit, values)
                if not success:
                    # TODO: Add a pwetty statys bar to report errors with
                    self.SetStatusText(status)
                    return

                x, y = success, status

                self.subplot.plot(x, y)
                legend.append(fit.name)
            except:
                pyfalog.warning(u"Invalid values in '{0}'", fit.name)
                self.SetStatusText(u"Invalid values in '%s'" % fit.name)
                self.canvas.draw()
                return

        if mpl_version < 2:
            if self.legendFix and len(legend) > 0:
                leg = self.subplot.legend(tuple(legend), "upper right", shadow=False)
                for t in leg.get_texts():
                    t.set_fontsize('small')

                for l in leg.get_lines():
                    l.set_linewidth(1)

            elif not self.legendFix and len(legend) > 0:
                leg = self.subplot.legend(tuple(legend), "upper right", shadow=False, frameon=False)
                for t in leg.get_texts():
                    t.set_fontsize('small')

                for l in leg.get_lines():
                    l.set_linewidth(1)
        elif mpl_version >= 2:
            legend2 = []
            legend_colors = {
                0: "blue",
                1: "orange",
                2: "green",
                3: "red",
                4: "purple",
                5: "brown",
                6: "pink",
                7: "grey",
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
        self.SetStatusText("")
        if event is not None:
            event.Skip()

    def onFieldChanged(self, event):
        self.draw()

    def AppendFitToList(self, fitID):
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit not in self.fits:
            self.fits.append(fit)

        self.fitList.fitList.update(self.fits)
        self.draw()

    def removeItem(self, event):
        row, _ = self.fitList.fitList.HitTest(event.Position)
        if row != -1:
            del self.fits[row]
            self.fitList.fitList.update(self.fits)
            self.draw()


class FitList(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        self.fitList = FitDisplay(self)
        self.mainSizer.Add(self.fitList, 1, wx.EXPAND)
        fitToolTip = wx.ToolTip("Drag a fit into this list to graph it")
        self.fitList.SetToolTip(fitToolTip)


class FitDisplay(gui.display.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name"]

    def __init__(self, parent):
        gui.display.Display.__init__(self, parent)
