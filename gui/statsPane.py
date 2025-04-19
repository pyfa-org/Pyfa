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
from service.settings import StatViewSettings
import gui.mainFrame
import gui.builtinStatsViews
import gui.globalEvents as GE
# import gui.builtinViews.fittingView as fv
from gui.statsView import StatsView
from gui.contextMenu import ContextMenu
from gui.toggle_panel import TogglePanel
from logbook import Logger

pyfalog = Logger(__name__)


class StatsPane(wx.Panel):
    AVAILIBLE_VIEWS = [
        "resources",
        "resistances",
        "recharge",
        "firepower",
        "outgoing",
        "capacitor",
        "targetingMisc",
        "price",
    ]

    # Don't have these....yet....
    '''
    "miningyield", "drones"
    ]
    '''

    DEFAULT_VIEWS = []

    settings = StatViewSettings.getInstance()

    for aView in AVAILIBLE_VIEWS:
        if settings.get(aView) == 2:
            DEFAULT_VIEWS.extend(["%sViewFull" % aView])
            pyfalog.debug("Setting full view for: {0}", aView)
        elif settings.get(aView) == 1:
            DEFAULT_VIEWS.extend(["%sViewMinimal" % aView])
            pyfalog.debug("Setting minimal view for: {0}", aView)
        elif settings.get(aView) == 0:
            pyfalog.debug("Setting disabled view for: {0}", aView)
        else:
            pyfalog.error("Unknown setting for view: {0}", aView)

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return
        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)
        for view in self.views:
            view.refreshPanel(fit)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Use 25% smaller fonts if MAC or force font size to 8 for msw/linux

        if "__WXMAC__" in wx.PlatformInfo:
            self.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        elif "__WXGTK__" in wx.PlatformInfo:
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
            contentPanel = tp.GetContentPanel()
            contentPanel.viewName = viewName

            try:
                view = StatsView.getView(viewName)(self)
                pyfalog.debug("Load view: {0}", viewName)
            except KeyError:
                pyfalog.error("Attempted to load an invalid view: {0}", viewName)

            self.nameViewMap[viewName] = view
            self.views.append(view)

            headerPanel = tp.GetHeaderPanel()

            view.populatePanel(contentPanel, headerPanel)
            tp.SetLabel(view.getHeaderText(None))
            view.refreshPanel(None)

            contentPanel.Bind(wx.EVT_CONTEXT_MENU, self.contextHandler(contentPanel, tp))

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

    def contextHandler(self, contentPanel, tp):
        viewName = contentPanel.viewName

        def handler(event):
            menu = ContextMenu.getMenu(self, None, None, (viewName,))

            if menu is not None:
                contentPanel.PopupMenu(menu)

            event.Skip()

        if ContextMenu.hasMenu(self, None, None, (viewName,)):
            sizer = tp.GetHeaderContentSizer()
            sizer.AddStretchSpacer()
            # Add menu
            header_menu = wx.StaticText(tp.GetHeaderPanel(), wx.ID_ANY, "\u2630", size=wx.Size((10, -1)))
            sizer.Add(header_menu , 0, wx.EXPAND | wx.RIGHT, 5)

            header_menu.Bind(wx.EVT_CONTEXT_MENU, handler)
            header_menu.Bind(wx.EVT_LEFT_UP, handler)

        return handler
