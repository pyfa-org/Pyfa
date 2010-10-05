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

import sys
import wx
import wx.lib.newevent
import service
import bitmapLoader
import gui.mainFrame
from gui.cachingImageList import CachingImageList
from gui.contextMenu import ContextMenu

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
        self.search = wx.SearchCtrl(p, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        sizer.Add(self.search, 1, wx.EXPAND | wx.TOP, 2)
        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 27))

        #Bind search
        self.search.Bind(wx.EVT_TEXT_ENTER, self.scheduleSearch)
        self.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.scheduleSearch)
        self.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.clearSearch)
        self.search.Bind(wx.EVT_TEXT, self.scheduleSearch)

        #Helper vars for search: INIT EM ALREADY
        self.searching = False
        self.searchResults = None

        self.searchTimer = wx.Timer()
        self.searchTimer.SetOwner(self)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        vbox.Add(self.splitter, 1, wx.EXPAND)

        self.marketView = MarketTree(self.splitter)
        listStyle = wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL
        self.itemView = wx.ListCtrl(self.splitter, style = listStyle)

        treeStyle = self.marketView.GetWindowStyleFlag()
        treeStyle |= wx.TR_HIDE_ROOT
        self.marketView.SetWindowStyleFlag(treeStyle)

        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE
        info.m_image = -1
        info.m_text = "Name"
        self.itemView.InsertColumnInfo(0, info)

        self.splitter.SplitHorizontally(self.marketView, self.itemView)
        self.splitter.SetMinimumPaneSize(250)

        self.marketRoot = self.marketView.AddRoot("Market")

        self.marketImageList = CachingImageList(16, 16)
        self.marketView.SetImageList(self.marketImageList)

        self.itemImageList = CachingImageList(16, 16)
        self.itemView.SetImageList(self.itemImageList, wx.IMAGE_LIST_SMALL)

        cMarket = service.Market.getInstance()

        root = cMarket.getMarketRoot()
        for id, name, iconFile in root:
            iconId = self.addMarketViewImage(iconFile)
            childId = self.marketView.AppendItem(self.marketRoot, name, iconId, data=wx.TreeItemData(id))
            self.marketView.AppendItem(childId, "dummy")

        self.marketView.SortChildren(self.marketRoot)

        #Bind our lookup method to when the tree gets expanded
        self.marketView.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        self.marketView.Bind(wx.EVT_TREE_SEL_CHANGED, self.selectionMade)

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

        #Bind context menus
        self.itemView.Bind(wx.EVT_CONTEXT_MENU, self.contextMenu)
        self.itemView.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def addMarketViewImage(self, iconFile):
        if iconFile is None:
            return -1

        return self.marketImageList.Add(iconFile, "pack")

    def addItemViewImage(self, iconFile):
        if iconFile is None:
            return -1
        
        return self.itemImageList.Add(iconFile, "pack")

    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.marketView.GetFirstChild(root)
        if self.marketView.GetItemText(child) == "dummy":
            cMarket = service.Market.getInstance()
            #A DUMMY! Keeeel!!! EBUL DUMMY MUST DIAF!
            self.marketView.Delete(child)

            #Add 'real stoof!' instead
            for id, name, iconFile, more in cMarket.getChildren(self.marketView.GetPyData(root)):
                iconId = self.addMarketViewImage(iconFile)
                childId = self.marketView.AppendItem(root, name, iconId, data=wx.TreeItemData(id))
                if more:
                    self.marketView.AppendItem(childId, "dummy")

            self.marketView.SortChildren(root)


    def selectionMade(self, event):
        self.itemView.DeleteAllItems()

        if self.searching:
            self.clearSearch(None, False)

        root = self.marketView.GetSelection()
        if root.IsOk():
            if self.marketView.GetChildrenCount(root) != 0:
                return

            cMarket = service.Market.getInstance()
            idNameMap = {}
            data, usedMetas = cMarket.getVariations(self.marketView.GetPyData(root))
            for id, name, iconFile in data:
                iconId = self.addItemViewImage(iconFile)
                index = self.itemView.InsertImageStringItem(sys.maxint, name, iconId)
                idNameMap[id] = name

                self.itemView.SetItemData(index, id)

            self.itemView.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
            self.itemView.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            width = self.itemView.GetColumnWidth(0)
            maxWidth = self.itemView.GetSize()[0]
            if maxWidth > width:
                self.itemView.SetColumnWidth(0, maxWidth)

            self.toggleButtons(usedMetas)

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

        if self.searching:
            self.filteredSearchAdd()
        else:
            self.selectionMade(event)

    def scheduleSearch(self, event):
        search = self.search.GetLineText(0)
        if len(search) < 3:
            self.clearSearch(event, False)
            return

        cMarket = service.Market.getInstance()
        if not self.searching:
            for name in ("normal", "faction", "complex", "officer"):
                getattr(self, name).SetValue(True)
                cMarket.activateMetaGroup(name)

        self.searching = True
        cMarket.searchItems(search, self.populateSearch)

    def clearSearch(self, event, clear=True):
        self.itemView.DeleteAllItems()
        if clear:
            self.search.Clear()

        cMarket = service.Market.getInstance()
        for name in ("normal", "faction", "complex", "officer"):
            btn = getattr(self, name)
            btn.Enable(True)
            btn.SetValue(False)
            cMarket.disableMetaGroup(btn.metaName)

        cMarket.activateMetaGroup("normal")
        self.normal.SetValue(True)

        self.searching = False

    def populateSearch(self, results):
        self.searchResults = results
        self.filteredSearchAdd()

    def toggleButtons(self, usedMetas):
        cMarket = service.Market.getInstance()
        for name in ("normal", "faction", "complex", "officer"):
            btn = getattr(self, name)
            btn.SetValue(False)
            btn.Enable(False)

        for meta in usedMetas:
            btn = getattr(self, cMarket.getMetaName(meta))
            btn.SetValue(cMarket.isMetaIdActive(meta))
            btn.Enable(True)

    def filteredSearchAdd(self):
        if self.searching is False:
            return

        self.itemView.Freeze()
        self.itemView.DeleteAllItems()

        idNameMap = {}
        idGroupMap = {}
        usedMetas = set()
        cMarket = service.Market.getInstance()
        for id, name, group, metaGroupID, iconFile in self.searchResults:
            usedMetas.add(metaGroupID)
            if cMarket.isMetaIdActive(metaGroupID):
                iconId = self.addItemViewImage(iconFile)
                index = self.itemView.InsertImageStringItem(sys.maxint, name, iconId)
                idNameMap[id] = name
                idGroupMap[id] = group
                self.itemView.SetItemData(index, id)

        #Gray out empty toggles
        self.toggleButtons(usedMetas)

        def sort(id1, id2):
            grp = cmp(idGroupMap[id1], idGroupMap[id2])
            if grp != 0:
                return grp

            return cmp(idNameMap[id1], idNameMap[id2])

        self.itemView.SortItems(sort)
        self.itemView.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        width = self.itemView.GetColumnWidth(0)
        maxWidth = self.itemView.GetSize()[0]
        if maxWidth > width:
            self.itemView.SetColumnWidth(0, maxWidth)

        self.itemView.Thaw()

    def contextMenu(self, event):
        #Check if something is selected, if so, spawn the menu for it
        sel = self.itemView.GetFirstSelected()
        selection = []
        cMarket = service.Market.getInstance()
        while sel != -1:
            itemId = self.itemView.GetItemData(sel)
            sel = self.itemView.GetNextSelected(sel)
            selection.append(cMarket.getItem(itemId))

        menu = ContextMenu.getMenu(selection, "item")
        self.PopupMenu(menu)

    def itemActivated(self, event):
        id = event.Item.GetData()
        if id != -1:
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=id))


class MarketTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)

    def OnEraseBackGround(self, event):
        #Prevent flicker by not letting the parent's method get called.
        pass
