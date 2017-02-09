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

from service.fit import Fit
import gui.mainFrame
import gui.builtinStatsViews
import gui.globalEvents as GE
# import gui.builtinViews.fittingView as fv
from gui.statsView import StatsView
from gui.contextMenu import ContextMenu
from gui.pyfatogglepanel import TogglePanel


class StatsPane(wx.Panel):
    DEFAULT_VIEWS = ["resourcesViewFull", "resistancesViewFull", "rechargeViewFull", "firepowerViewFull",
                     "capacitorViewFull", "targetingmiscViewFull",
                     "priceViewFull"]

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)
        for view in self.views:
            view.refreshPanel(fit)
        event.Skip()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Use 25% smaller fonts if MAC or force font size to 8 for msw/linux

        if "__WXMAC__" in wx.PlatformInfo:
            self.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        else:
            standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            standardFont.SetPointSize(8)
            self.SetFont(standardFont)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.views = []
        self.nameViewMap = {}
        maxviews = len(self.DEFAULT_VIEWS)
        i = 0
        for viewName in self.DEFAULT_VIEWS:
            tp = TogglePanel(self)
            contentPanel = tp.GetContentPane()
            contentPanel.viewName = viewName

            view = StatsView.getView(viewName)(self)
            self.nameViewMap[viewName] = view
            self.views.append(view)

            headerPanel = tp.GetHeaderPanel()

            view.populatePanel(contentPanel, headerPanel)
            tp.SetLabel(view.getHeaderText(None))
            view.refreshPanel(None)

            contentPanel.Bind(wx.EVT_RIGHT_DOWN, self.contextHandler(contentPanel))
            for child in contentPanel.GetChildren():
                child.Bind(wx.EVT_RIGHT_DOWN, self.contextHandler(contentPanel))

            mainSizer.Add(tp, 0, wx.EXPAND | wx.LEFT, 3)
            if i < maxviews - 1:
                mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.HORIZONTAL), 0,
                              wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 2)
            i += 1
            tp.OnStateChange(tp.GetBestSize())

        width, height = self.GetSize()
        self.SetMinSize((width + 9, -1))

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    @staticmethod
    def contextHandler(contentPanel):
        viewName = contentPanel.viewName

        def handler(event):
            menu = ContextMenu.getMenu(None, (viewName,))
            if menu is not None:
                contentPanel.PopupMenu(menu)

            event.Skip()

        return handler
