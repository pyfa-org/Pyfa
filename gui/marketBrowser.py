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

import gui.display as d
from gui.cachingImageList import CachingImageList
from gui.contextMenu import ContextMenu
import wx
import service

ItemSelected, ITEM_SELECTED = wx.lib.newevent.NewEvent()

class MarketBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        #Add a search button on top

        #Add a WHOLE panel for ONE SINGLE search button
        #We have to be able to give the search more size, which can't be done in another way.
        #(That I found)
        p = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(sizer)

        vbox.Add(p, 0, wx.EXPAND)
        self.search = SearchBox(p)
        sizer.Add(self.search, 1, wx.ALIGN_CENTER_VERTICAL | wx.TOP, 2)
        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 27))

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)
        vbox.Add(self.splitter, 1, wx.EXPAND)

        self.marketView = MarketTree(self.splitter, self)
        self.itemView = ItemView(self.splitter, self)

        self.splitter.SplitHorizontally(self.marketView, self.itemView)
        self.splitter.SetMinimumPaneSize(250)

        cMarket = service.Market.getInstance()
        # Setup our buttons for metaGroup selection
        # Same fix as for search box on macs,
        # need some pixels of extra space or everything clips and is ugly
        p = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(box)
        vbox.Add(p, 0, wx.EXPAND)
        for name in ("normal", "faction", "complex", "officer"):
            btn = wx.ToggleButton(p, wx.ID_ANY, name.capitalize(), style=wx.BU_EXACTFIT)
            setattr(self, name, btn)
            box.Add(btn, 1, wx.ALIGN_CENTER)
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.toggleMetagroup)
            btn.metaName = name

        self.normal.SetValue(True)
        cMarket.activateMetaGroup("normal")
        p.SetMinSize((wx.SIZE_AUTO_WIDTH, btn.GetSize()[1] + 5))

    def toggleMetagroup(self, event):
        ctrl = wx.GetMouseState().ControlDown()
        cMarket = service.Market.getInstance()
        btn = event.EventObject
        if not ctrl:
            for name in ("normal", "faction", "complex", "officer"):
                button = getattr(self, name)
                button.SetValue(False)
                button.Enable(True)

                cMarket.disableMetaGroup(name)

            btn.SetValue(True)
            cMarket.activateMetaGroup(btn.metaName)
        else:
            # Note: using the old value might seem weird,
            # But the button hasn't been toggled by wx yet
            target = btn.GetValue()
            btn.SetValue(target)
            if target:
                cMarket.activateMetaGroup(btn.metaName)
            else:
                cMarket.disableMetaGroup(btn.metaName)

        if self.itemView.searching:
            self.itemView.filteredSearchAdd()
        else:
            self.itemView.selectionMade(event)

    def jump(self, item):
        self.marketView.jump(item)


class SearchBox(wx.SearchCtrl):
    def __init__(self, parent):
        wx.SearchCtrl.__init__(self, parent, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.ShowCancelButton(True)

class MarketTree(wx.TreeCtrl):
    def __init__(self, parent, marketBrowser):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        self.root = self.AddRoot("CHRISTMAS TREE!")
        self.marketBrowser = marketBrowser

        self.imageList = CachingImageList(16, 16)
        self.SetImageList(self.imageList)

        cMarket = service.Market.getInstance()

        root = cMarket.getMarketRoot()
        for id, name, iconFile in root:
            iconId = self.addImage(iconFile)
            childId = self.AppendItem(self.root, name, iconId, data=wx.TreeItemData(id))
            self.AppendItem(childId, "dummy")

        self.SortChildren(self.root)

        #Bind our lookup method to when the tree gets expanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

    def addImage(self, iconFile):
        if iconFile is None:
            return -1

        return self.imageList.Add(iconFile, "pack")

    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.GetFirstChild(root)
        if self.GetItemText(child) == "dummy":
            cMarket = service.Market.getInstance()
            #A DUMMY! Keeeel!!! EBUL DUMMY MUST DIAF!
            self.Delete(child)

            #Add 'real stoof!' instead
            for id, name, iconFile, more in cMarket.getChildren(self.GetPyData(root)):
                iconId = self.addImage(iconFile)
                childId = self.AppendItem(root, name, iconId, data=wx.TreeItemData(id))
                if more:
                    self.AppendItem(childId, "dummy")

            self.SortChildren(root)

    def jump(self, item):
        cMarket = service.Market.getInstance()
        # Refetch items, else it'll try to reuse the object fetched in the other thread
        # Which makes it go BOOM CRACK DOOM
        item = cMarket.getItem(item.ID)
        mg = item.marketGroup
        if mg is None and item.metaGroup is not None:
            mg = item.metaGroup.parent.marketGroup
            for btn in ("normal", "faction", "complex", "officer"):
                getattr(self.marketBrowser, btn).SetValue(False)
                cMarket.disableMetaGroup(btn)

            metaGroup = cMarket.getMetaName(item.metaGroup.ID)

            getattr(self.marketBrowser, metaGroup).SetValue(True)
            cMarket.activateMetaGroup(metaGroup)
            self.marketBrowser.itemView.searching = False

        if mg is None:
            return

        jumpList = []
        while mg is not None:
            jumpList.append(mg.ID)
            mg = mg.parent

        cMarket.MARKET_GROUPS
        for id in cMarket.MARKET_GROUPS:
            if id in jumpList:
                jumpList = jumpList[:jumpList.index(id)+1]

        item = self.root
        for i in range(len(jumpList) -1, -1, -1):
            target = jumpList[i]
            child, cookie = self.GetFirstChild(item)
            while self.GetItemPyData(child) != target:
                child, cookie = self.GetNextChild(item, cookie)

            item = child
            self.Expand(item)

        self.SelectItem(item)
        self.marketBrowser.itemView.searching = False

class ItemView(d.Display):
    DEFAULT_COLS = ["Name"]

    def __init__(self, parent, marketBrowser):
        d.Display.__init__(self, parent)
        marketBrowser.Bind(wx.EVT_TREE_SEL_CHANGED, self.selectionMade)
        self.searching = False
        self.marketBrowser = marketBrowser
        self.marketView = marketBrowser.marketView

        #Make sure our search actualy does intresting stuff
        self.marketBrowser.search.Bind(wx.EVT_TEXT_ENTER, self.scheduleSearch)
        self.marketBrowser.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.scheduleSearch)
        self.marketBrowser.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.clearSearch)
        self.marketBrowser.search.Bind(wx.EVT_TEXT, self.scheduleSearch)

        #Make sure WE do intresting stuff TOO
        self.Bind(wx.EVT_CONTEXT_MENU, self.contextMenu)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)

    def itemActivated(self, event):
        #Check if something is selected, if so, spawn the menu for it
        sel = self.GetFirstSelected()
        if sel == -1:
            return

        wx.PostEvent(self.mainFrame, ItemSelected(itemID=self.active[sel].ID))

    def selectionMade(self, event):
        if self.searching:
            self.clearSearch(None, False)

        root = self.marketView.GetSelection()
        if root.IsOk():
            if self.marketView.GetChildrenCount(root) != 0:
                return

            cMarket = service.Market.getInstance()
            items, usedMetas = cMarket.getVariations(self.marketView.GetPyData(root))
            self.update(items)
            self.toggleButtons(usedMetas)

    def clearSearch(self, event=None, clear=True):
        self.DeleteAllItems()
        if clear:
            self.marketBrowser.search.Clear()

        cMarket = service.Market.getInstance()
        for name in ("normal", "faction", "complex", "officer"):
            btn = getattr(self.marketBrowser, name)
            btn.Enable(True)
            btn.SetValue(False)
            cMarket.disableMetaGroup(btn.metaName)

        cMarket.activateMetaGroup("normal")
        self.marketBrowser.normal.SetValue(True)

        self.searching = False

    def scheduleSearch(self, event):
        search = self.marketBrowser.search.GetLineText(0)
        if len(search) < 3:
            self.clearSearch(event, False)
            return

        cMarket = service.Market.getInstance()
        if not self.searching:
            for name in ("normal", "faction", "complex", "officer"):
                getattr(self.marketBrowser, name).SetValue(True)
                cMarket.activateMetaGroup(name)

        self.searching = True
        cMarket.searchItems(search, self.populateSearch)

    def populateSearch(self, results):
        self.filteredSearchAdd(*results)

    def itemFilter(self, item):
        pass

    def filteredSearchAdd(self, items=None, usedMetas=None):
        if self.searching is False:
            return

        self.items = items if items is not None else self.items
        self.usedMetas = usedMetas if usedMetas is not None else self.usedMetas
        sMarket = service.Market.getInstance()

        self.update(sMarket.filterItems(self.items))

        #Gray out empty toggles
        self.toggleButtons(self.usedMetas)

    def toggleButtons(self, usedMetas):
        cMarket = service.Market.getInstance()
        for name in ("normal", "faction", "complex", "officer"):
            btn = getattr(self.marketBrowser, name)
            btn.SetValue(False)
            btn.Enable(False)

        for meta in usedMetas:
            btn = getattr(self.marketBrowser, cMarket.getMetaName(meta))
            btn.SetValue(cMarket.isMetaIdActive(meta))
            btn.Enable(True)

    def contextMenu(self, event):
        #Check if something is selected, if so, spawn the menu for it
        sel = self.GetFirstSelected()
        if sel == -1:
            return

        menu = ContextMenu.getMenu(self.active[sel], "item" if self.searching is False else "itemSearch")
        self.PopupMenu(menu)

    def itemSort(self, item):
        if item.metaGroup is None:
            return (item.name, 0, item.name)
        else:
            return (item.metaGroup.parent.name, item.metaGroup.ID , item.name)

    def populate(self, stuff):
        stuff.sort(key=self.itemSort)
        self.active = stuff
        d.Display.populate(self, stuff)

    def refresh(self, stuff):
        stuff.sort(key=self.itemSort)
        d.Display.refresh(self, stuff)
