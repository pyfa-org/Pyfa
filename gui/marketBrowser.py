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

from gui.builtinMarketBrowser.searchBox import SearchBox
from gui.builtinMarketBrowser.itemView import ItemView
from gui.builtinMarketBrowser.metaButton import MetaButton
from gui.builtinMarketBrowser.marketTree import MarketTree
from service.market import Market
from service.settings import MarketPriceSettings

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

        # Grab service stuff and create child objects
        self.sMkt = Market.getInstance()
        self.settings = MarketPriceSettings.getInstance()
        self.__mode = 'normal'
        self.__normalBtnMap = {}
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
        clickedBtn = event.EventObject

        if wx.GetMouseState().GetModifiers() == wx.MOD_CONTROL:
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
        self.mode = 'normal'
        self.marketView.jump(item)
        setting = self.settings.get('marketMGJumpMode')
        itemMetaCat = self.sMkt.META_MAP_REVERSE[self.sMkt.getMetaGroupIdByItem(item)]
        # Enable item meta category
        if setting == 1:
            btn = getattr(self, itemMetaCat)
            if not btn.GetValue():
                btn.setUserSelection(True)
        # Enable item meta category, disable others
        elif setting == 2:
            tgtBtn = getattr(self, itemMetaCat)
            if not tgtBtn.GetValue():
                tgtBtn.setUserSelection(True)
            for btn in self.metaButtons:
                if btn is tgtBtn:
                    continue
                if btn.GetValue:
                    btn.setUserSelection(False)
        # Enable all meta categories
        elif setting == 3:
            for btn in self.metaButtons:
                if not btn.GetValue():
                    btn.setUserSelection(True)
        self.itemView.selectionMade('jump')

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, newMode):
        oldMode = self.__mode
        if newMode == oldMode != 'search':
            return
        # Store meta button states when switching from normal
        if oldMode == 'normal':
            self.__normalBtnMap.clear()
            for btn in self.metaButtons:
                self.__normalBtnMap[btn] = btn.userSelected
        if newMode == 'search':
            self.marketView.UnselectAll()
        setting = self.settings.get('marketMGSearchMode')
        # We turn on all meta buttons for the duration of search/recents
        if setting == 1:
            if newMode in ('search', 'recent'):
                for btn in self.metaButtons:
                    btn.setUserSelection(True)
            if newMode == 'normal':
                for btn, state in self.__normalBtnMap.items():
                    btn.setUserSelection(state)
        # We turn on all meta buttons permanently
        if setting == 2:
            for btn in self.metaButtons:
                btn.setUserSelection(True)
        self.__mode = newMode

