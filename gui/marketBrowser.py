#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import sys
import wx
import controller
import bitmapLoader

class MarketBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        #Add a search button on top
        p = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(sizer)
        vbox.Add(p, 0, wx.EXPAND)
        self.search = wx.SearchCtrl(p, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        sizer.Add(self.search, 1, wx.EXPAND)
        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 25))

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        vbox.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(vbox)

        self.marketView = wx.TreeCtrl(self.splitter)
        listStyle = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL
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

        self.marketImageList = wx.ImageList(16, 16)
        self.marketView.SetImageList(self.marketImageList)

        self.itemImageList = wx.ImageList(16, 16)
        self.itemView.SetImageList(self.itemImageList, wx.IMAGE_LIST_SMALL)

        cMarket = controller.Market.getInstance()

        root = cMarket.getMarketRoot()
        for id, name, iconFile in root:
            iconId = self.addMarketViewImage(iconFile)
            childId = self.marketView.AppendItem(self.marketRoot, name, iconId, data=wx.TreeItemData(id))
            self.marketView.AppendItem(childId, "dummy")

        self.marketView.SortChildren(self.marketRoot)

        #Bind our lookup method to when the tree gets expanded
        self.marketView.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        self.marketView.Bind(wx.EVT_TREE_SEL_CHANGED, self.selectionMade)

        #Setup our buttons for metaGroup selection
        box = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(box, 0)
        for name in ("normal", "faction", "complex", "officer"):
            btn = wx.Button(self, wx.ID_ANY, name.capitalize(), style=wx.BU_EXACTFIT)
            setattr(self, name, btn)
            box.Add(btn, 0)

    def addMarketViewImage(self, iconFile):
        if iconFile is None:
            return -1
        bitmap = bitmapLoader.getBitmap(iconFile, "pack")
        if bitmap is None:
            return -1
        else:
            return self.marketImageList.Add(bitmap)

    def addItemViewImage(self, iconFile):
        if iconFile is None:
            return -1
        bitmap = bitmapLoader.getBitmap(iconFile, "pack")
        if bitmap is None:
            return -1
        else:
            return self.itemImageList.Add(bitmap)

    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.marketView.GetFirstChild(root)
        if self.marketView.GetItemText(child) == "dummy":
            cMarket = controller.Market.getInstance()
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
        self.itemImageList.RemoveAll()

        root = event.Item
        if self.marketView.GetChildrenCount(root) != 0:
            return

        cMarket = controller.Market.getInstance()
        idNameMap = {}

        for id, name, iconFile in cMarket.getItems(self.marketView.GetPyData(root)):
            iconId = self.addItemViewImage(iconFile)
            index = self.itemView.InsertImageStringItem(sys.maxint, name, iconId)
            idNameMap[id] = name
            self.itemView.SetItemData(index, id)

        self.itemView.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
        self.itemView.SetColumnWidth(0, wx.LIST_AUTOSIZE)
