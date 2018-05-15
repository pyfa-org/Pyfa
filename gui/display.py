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
import gui.mainFrame
from gui.viewColumn import ViewColumn
from gui.cachingImageList import CachingImageList


class Display(wx.ListCtrl):
    DEFAULT_COLS = None

    def __init__(self, parent, size=wx.DefaultSize, style=0):

        wx.ListCtrl.__init__(self, parent, size=size, style=wx.LC_REPORT | style)
        self.imageList = CachingImageList(16, 16)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        self.activeColumns = []
        self.columnsMinWidth = []
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.resizeChecker)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.resizeSkip)

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
                    if type == bool and isinstance(value, str):
                        value = bool(value) if value.lower() != "false" and value != "0" else False
                    paramDict[name] = value
                col = colClass(self, paramDict)
            else:
                col = ViewColumn.getColumn(colName)(self, None)

            self.addColumn(i, col)
            self.columnsMinWidth.append(self.GetColumnWidth(i))
            i += 1

        info = wx.ListItem()
        # noinspection PyPropertyAccess
        info.m_mask = wx.LIST_MASK_WIDTH
        self.InsertColumn(i, info)
        self.SetColumnWidth(i, 0)

        self.imageListBase = self.imageList.ImageCount

    # Override native HitTestSubItem (doesn't work as it should on GTK)
    # Source: ObjectListView

    def HitTestSubItem(self, pt):
        """
        Return a tuple indicating which (item, subItem) the given pt (client coordinates) is over.

        This uses the built-in version on Windows, and poor mans replacement on other platforms.
        """
        # The buildin version works on Windows

        if wx.Platform == "__WXMSW__":
            return wx.ListCtrl.HitTestSubItem(self, pt)

        (rowIndex, flags) = self.HitTest(pt)

        # Did the point hit any item?
        if (flags & wx.LIST_HITTEST_ONITEM) == 0:
            return -1, 0, -1

        # If it did hit an item and we are not in report mode, it must be the primary cell
        if not self.InReportView():
            return rowIndex, wx.LIST_HITTEST_ONITEM, 0

        # Find which subitem is hit
        right = 0
        scrolledX = self.GetScrollPos(wx.HORIZONTAL) * wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y) + pt.x
        for i in range(self.GetColumnCount()):
            left = right
            right += self.GetColumnWidth(i)
            if scrolledX < right:
                if (scrolledX - left) < self.imageList.GetSize(0)[0]:
                    flag = wx.LIST_HITTEST_ONITEMICON
                else:
                    flag = wx.LIST_HITTEST_ONITEMLABEL
                return rowIndex, flag, i

        return rowIndex, 0, -1

    # noinspection PyPropertyAccess
    def addColumn(self, i, col):
        self.activeColumns.append(col)
        info = wx.ListItem()
        info.SetMask(col.mask | wx.LIST_MASK_FORMAT | wx.LIST_MASK_WIDTH)
        info.SetImage(col.imageId)
        info.SetText(col.columnText)
        info.SetWidth(-1)
        info.SetAlign(wx.LIST_FORMAT_LEFT)
        self.InsertColumn(i, info)
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
        wx.CallAfter(self.checkColumnSize, column)
        event.Skip()

    def resizeSkip(self, event):
        column = event.GetColumn()
        if column > len(self.activeColumns) - 1:
            self.SetColumnWidth(column, 0)
            event.Veto()
            return
        # colItem = self.activeColumns[column]
        if self.activeColumns[column].maxsize != -1:
            event.Veto()
        else:
            event.Skip()

    def checkColumnSize(self, column):
        colItem = self.activeColumns[column]
        if self.GetColumnWidth(column) < self.columnsMinWidth[column]:
            self.SetColumnWidth(column, self.columnsMinWidth[column])
        colItem.resized = True

    def getLastItem(self, state=wx.LIST_STATE_DONTCARE):
        lastFound = -1
        while True:
            index = self.GetNextItem(lastFound, wx.LIST_NEXT_ALL, state)
            if index == -1:
                break
            else:
                lastFound = index

        return lastFound

    def deselectItems(self):
        sel = self.GetFirstSelected()
        while sel != -1:
            self.SetItemState(sel, 0, wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED)
            sel = self.GetNextSelected(sel)

    def populate(self, stuff):

        if stuff is not None:
            listItemCount = self.GetItemCount()
            stuffItemCount = len(stuff)

            if listItemCount < stuffItemCount:
                for i in range(stuffItemCount - listItemCount):
                    self.InsertItem(self.GetItemCount(), "")

            if listItemCount > stuffItemCount:
                if listItemCount - stuffItemCount > 20 > stuffItemCount:
                    self.DeleteAllItems()
                    for i in range(stuffItemCount):
                        self.InsertItem(self.GetItemCount(), "")
                else:
                    for i in range(listItemCount - stuffItemCount):
                        self.DeleteItem(self.getLastItem())
                    self.Refresh()

    def refresh(self, stuff):
        if stuff is None:
            return

        item = -1
        for id_, st in enumerate(stuff):

            item = self.GetNextItem(item)

            for i, col in enumerate(self.activeColumns):
                colItem = self.GetItem(item, i)
                oldText = colItem.GetText()
                oldImageId = colItem.GetImage()
                newText = col.getText(st)
                if newText is False:
                    col.delayedText(st, self, colItem)
                    newText = "\u21bb"

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

                self.SetItemData(item, id_)

        # self.Freeze()
        if 'wxMSW' in wx.PlatformInfo:
            for i, col in enumerate(self.activeColumns):
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
                        # self.Thaw()

    def update(self, stuff):
        self.populate(stuff)
        self.refresh(stuff)

    def getColumn(self, point):
        row, _, col = self.HitTestSubItem(point)
        return col
