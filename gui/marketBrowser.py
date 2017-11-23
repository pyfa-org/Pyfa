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

from service.market import Market

from gui.builtinMarketBrowser.searchBox import SearchBox
from gui.builtinMarketBrowser.itemView import ItemView
from gui.builtinMarketBrowser.metaButton import MetaButton
from gui.builtinMarketBrowser.marketTree import MarketTree

from logbook import Logger

pyfalog = Logger(__name__)


class MarketBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pyfalog.debug("Initialize marketBrowser")
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        # Add a search box on top
        self.search = SearchBox(self)
        vbox.Add(self.search, 0, wx.EXPAND)

        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        vbox.Add(self.splitter, 1, wx.EXPAND)

        # Grab market service instance and create child objects
        self.sMkt = Market.getInstance()
        self.searchMode = False
        self.marketView = MarketTree(self.splitter, self)
        self.itemView = ItemView(self.splitter, self)

        self.splitter.SplitHorizontally(self.marketView, self.itemView)
        self.splitter.SetMinimumPaneSize(250)

        # Setup our buttons for metaGroup selection
        # Same fix as for search box on macs,
        # need some pixels of extra space or everything clips and is ugly
        p = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(box)
        vbox.Add(p, 0, wx.EXPAND)
        self.metaButtons = []
        btn = None
        for name in list(self.sMkt.META_MAP.keys()):
            btn = MetaButton(p, wx.ID_ANY, name.capitalize(), style=wx.BU_EXACTFIT)
            setattr(self, name, btn)
            box.Add(btn, 1, wx.ALIGN_CENTER)
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.toggleMetaButton)
            btn.metaName = name
            self.metaButtons.append(btn)
        # Make itemview to set toggles according to list contents
        self.itemView.setToggles()

        p.SetMinSize((wx.SIZE_AUTO_WIDTH, btn.GetSize()[1] + 5))

    def toggleMetaButton(self, event):
        """Process clicks on toggle buttons"""
        mstate = wx.GetMouseState()
        clickedBtn = event.EventObject

        if mstate.cmdDown:
            activeBtns = [btn for btn in self.metaButtons if btn.GetValue()]
            if activeBtns:
                clickedBtn.setUserSelection(clickedBtn.GetValue())
                self.itemView.filterItemStore()
            else:
                # Do 'nothing' if we're trying to turn last active button off
                # Keep button in the same state
                clickedBtn.setUserSelection(True)
        else:
            for btn in self.metaButtons:
                btn.setUserSelection(btn == clickedBtn)

            self.itemView.filterItemStore()

    def jump(self, item):
        self.marketView.jump(item)
