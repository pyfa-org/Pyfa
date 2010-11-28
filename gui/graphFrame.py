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
import gui.display

try:
    import matplotlib as mpl
    mpl.use('wxagg')
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    from matplotlib.figure import Figure
    enabled = True
except:
    print "Problems importing matplotlib; continuing without graphs"
    enabled = False

from gui.graph import Graph
import service
import gui.mainFrame

class GraphFrame(wx.Frame):
    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FRAME_FLOAT_ON_PARENT):
        wx.Frame.__init__(self, parent, title=u"pyfa: Graph Generator", style=style, size=(520, 390))

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("graphs_small", "icons"))
        self.SetIcon(i)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.CreateStatusBar()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        sFit = service.Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())
        self.fits = [fit] if fit is not None else []
        self.fitList = FitList(self)
        self.fitList.SetMinSize((270, -1))

        self.fitList.fitList.update(self.fits)

        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.mainSizer.Add(self.graphSelection, 0, wx.EXPAND)

        self.figure = Figure(figsize=(4, 3))

        rgbtuple = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ).Get()
        clr = [c/255. for c in rgbtuple]
        self.figure.set_facecolor( clr )
        self.figure.set_edgecolor( clr )

        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour( wx.Colour( *rgbtuple ) )

        self.subplot = self.figure.add_subplot(111)
        self.subplot.grid(True)

        self.mainSizer.Add(self.canvas, 1, wx.EXPAND)
        self.mainSizer.Add(wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL ), 0 , wx.EXPAND)

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
        self.sl1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.mainSizer.Add(self.sl1,0, wx.EXPAND)
        self.mainSizer.Add(self.fitList, 0, wx.EXPAND)

        self.fitList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.mainFrame.Bind(gui.builtinViews.fittingView.FIT_CHANGED, self.draw)
        self.Bind(wx.EVT_CLOSE, self.close)

        self.Fit()
        self.SetMinSize(self.GetSize())

    def handleDrag(self, type, fitID):
        if type == "fit":
            self.AppendFitToList(fitID)

    def close(self, event):
        self.fitList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.removeItem)
        self.mainFrame.Unbind(gui.builtinViews.fittingView.FIT_CHANGED, handler=self.draw)
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

        #Setup textboxes
        for field, defaultVal in view.getFields().iteritems():

            textBox = wx.TextCtrl(self.gridPanel, wx.ID_ANY, style=0)
            self.fields[field] = textBox
            textBox.Bind(wx.EVT_TEXT, self.onFieldChanged)
            sizer.Add(textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL  | wx.ALL, 3)
            if defaultVal is not None:
                if not isinstance(defaultVal, basestring):
                    defaultVal = ("%f" % defaultVal).rstrip("0")
                    if defaultVal[-1:] == ".":
                        defaultVal = defaultVal + "0"

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

            imgLabelSizer.Add(wx.StaticText(self.gridPanel, wx.ID_ANY, label), 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
            sizer.Add(imgLabelSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.draw()

    def draw(self, event=None):
        values = self.getValues()
        view = self.getView()
        self.subplot.clear()
        self.subplot.grid(True)

        for fit in self.fits:
            try:
                success, status = view.getPoints(fit, values)
                if not success:
                    #TODO: Add a pwetty statys bar to report errors with
                    self.SetStatusText(status)
                    return

                x, y = success, status

                self.subplot.plot(x, y)
            except:
                self.SetStatusText("Invalid values in '%s'" % fit.name)

        self.canvas.draw()
        self.SetStatusText("")
        if event is not None:
            event.Skip()

    def onFieldChanged(self, event):
        self.draw()

    def AppendFitToList(self, fitID):
        sFit = service.Fit.getInstance()
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

