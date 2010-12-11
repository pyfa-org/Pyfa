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
import gui.mainFrame

from gui.viewColumn import ViewColumn
from gui.cachingImageList import CachingImageList

class Display(wx.ListCtrl):
    def __init__(self, parent, size = wx.DefaultSize, style = 0):

        wx.ListCtrl.__init__(self, parent,size = size, style=wx.LC_REPORT |  style )
        self.imageList = CachingImageList(16, 16)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        self.activeColumns = []
        self.columnsMinWidth = []
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.resizeChecker)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.resizeSkip)

        if "wxMSW" in wx.PlatformInfo:
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBk)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        i = 0
        for colName in self.DEFAULT_COLS:
            if ":" in colName:
                colName, params = colName.split(":", 1)
                params = params.split(",")
                colClass = ViewColumn.getColumn(colName)
                paramList = colClass.getParameters()
                paramDict = {}
                for x, param in enumerate(paramList):
                    name, type, defaultValue = param
                    value = params[x] if len(params) > x else defaultValue
                    value = value if value != "" else defaultValue
                    if type == bool and isinstance(value, basestring):
                        value = bool(value) if value.lower() != "false" and value != "0" else False
                    paramDict[name] = value
                col = colClass(self, paramDict)
            else:
                col = ViewColumn.getColumn(colName)(self, None)

            self.addColumn(i, col)
            self.columnsMinWidth.append(self.GetColumnWidth(i))
            i += 1

        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_WIDTH
        self.InsertColumnInfo(i, info)
        self.SetColumnWidth(i, 0)

        self.imageListBase = self.imageList.ImageCount


    def OnEraseBk(self,event):
        if self.GetItemCount() >0:
            width, height = self.GetClientSize()
            dc = event.GetDC()

            dc.DestroyClippingRegion()
            dc.SetClippingRegion(0, 0, width, height)
            x,y,w,h = dc.GetClippingBox()

            topItem = self.GetTopItem()
            bottomItem = topItem + self.GetCountPerPage()

            if bottomItem >= self.GetItemCount():
               bottomItem = self.GetItemCount() - 1

            topRect = self.GetItemRect(topItem, wx.LIST_RECT_LABEL)
            bottomRect = self.GetItemRect(bottomItem, wx.LIST_RECT_BOUNDS)


            items_rect = wx.Rect(topRect.left, 0, bottomRect.right - topRect.left, bottomRect.bottom )

            updateRegion = wx.Region(x,y,w,h)
            updateRegion.SubtractRect(items_rect)

            dc.DestroyClippingRegion()
            dc.SetClippingRegionAsRegion(updateRegion)

            dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.SOLID))
            dc.Clear()

            dc.DestroyClippingRegion()

        else:
            event.Skip()

    def addColumn(self, i, col):
        self.activeColumns.append(col)
        info = wx.ListItem()
        info.m_mask = col.mask | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH
        info.m_image = col.imageId
        info.m_text = col.columnText
        info.m_width = -1
        info.m_format = wx.LIST_FORMAT_LEFT
        self.InsertColumnInfo(i, info)
        col.resized = False
        if i == 0 and col.size != wx.LIST_AUTOSIZE_USEHEADER:
            col.size += 4
        self.SetColumnWidth(i, col.size)

    def getColIndex(self, colClass):
        for i, col in enumerate(self.activeColumns):
            if col.__class__ == colClass:
                return i

        return None

    def resizeChecker(self, event):
        # we veto header cell resize by default till we find a way
        # to assure a minimal size for the resized header cell
        column = event.GetColumn()
        wx.CallAfter(self.checkColumnSize,column)
        event.Skip()

    def resizeSkip(self, event):
        column = event.GetColumn()
        if column > len (self.activeColumns)-1:
            self.SetColumnWidth(column, 0)
            event.Veto()
            return
        colItem = self.activeColumns[column]
        if self.activeColumns[column].maxsize != -1:
            event.Veto()
        else:
            event.Skip()

    def checkColumnSize(self,column):
        colItem = self.activeColumns[column]
        if self.GetColumnWidth(column) < self.columnsMinWidth[column]:
            self.SetColumnWidth(column,self.columnsMinWidth[column])
        colItem.resized = True

    def getLastItem( self, state =  wx.LIST_STATE_DONTCARE):
            lastFound = -1
            while True:
                    index = self.GetNextItem(
                            lastFound,
                            wx.LIST_NEXT_ALL,
                            state,
                    )
                    if index == -1:
                            break
                    else:
                            lastFound = index

            return lastFound

    def populate(self, stuff):
        selection = []


#        sel = self.GetFirstSelected()
#        while sel != -1:
#            selection.append(sel)
#            sel = self.GetNextSelected(sel)

#        self.DeleteAllItems()

        if stuff is not None:
            listItemCount = self.GetItemCount()
            stuffItemCount = len(stuff)

            if listItemCount < stuffItemCount:
                for i in xrange(stuffItemCount - listItemCount):
                    index = self.InsertStringItem(sys.maxint, "")

            if listItemCount > stuffItemCount:
                if listItemCount - stuffItemCount > 20 and stuffItemCount < 20:
                    self.DeleteAllItems()
                    for i in xrange(stuffItemCount):
                        index = self.InsertStringItem(sys.maxint, "")
                else:
                    for i in xrange(listItemCount - stuffItemCount):
                        self.DeleteItem(self.getLastItem())
                    self.Refresh()



#        for sel in selection:
#            self.Select(sel)

    def refresh(self, stuff):
        if stuff == None:
            return

        item = -1
        for id, st in enumerate(stuff):

            item = self.GetNextItem(item)

            for i, col in enumerate(self.activeColumns):
                colItem = self.GetItem(item, i)
                oldText = colItem.GetText()
                oldImageId = colItem.GetImage()
                newText = col.getText(st)
                if newText is False:
                    col.delayedText(st, self, colItem)
                    newText = ""

                newImageId = col.getImageId(st)

                colItem.SetText(newText)
                colItem.SetImage(newImageId)

                mask = 0

                if oldText != newText:
                    mask |= wx.LIST_MASK_TEXT
                    colItem.SetText(newText)
                if oldImageId != newImageId:
                    mask |= wx.LIST_MASK_IMAGE
                    colItem.SetImage(newImageId)

                if mask:
                    colItem.SetMask(mask)
                    self.SetItem(colItem)

                self.SetItemData(item, id)

#        self.Freeze()
        if 'wxMSW' in wx.PlatformInfo:
            for i,col in enumerate(self.activeColumns):
                if not col.resized:
                    self.SetColumnWidth(i, col.size)
        else:
            for i, col in enumerate(self.activeColumns):
                if not col.resized:
                    if col.size == wx.LIST_AUTOSIZE_USEHEADER:
                        self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
                        headerWidth = self.GetColumnWidth(i)
                        self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
                        baseWidth = self.GetColumnWidth(i)
                        if baseWidth < headerWidth:
                            self.SetColumnWidth(i, headerWidth)
                    else:
                        self.SetColumnWidth(i, col.size)
#        self.Thaw()



    def update(self, stuff):
        self.populate(stuff)
        self.refresh(stuff)

    def getColumn(self, point):
        x = point[0]
        total = 0
        for col in xrange(self.GetColumnCount()):
            total += self.GetColumnWidth(col)
            if total >= x:
                return col
