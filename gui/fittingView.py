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

import wx

import gui.builtinViewColumns
from gui.builtinViewColumns import *

class FittingView(wx.ListCtrl):
    DEFAULT_COLS = ["Module state", "Module name/slot"]
    def __init__(self, parent):
        listStyle = wx.LC_REPORT | wx.BORDER_NONE
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=listStyle)

        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        self.activeColumns = []
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.resizeChecker)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.dragCheck)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.dragCheck)
        i = 0
        for colName in FittingView.DEFAULT_COLS:
            col = gui.builtinViewColumns.getColumn(colName)(self, None)
            self.activeColumns.append(col)

            info = wx.ListItem()
            info.m_mask = col.mask
            info.m_image = col.imageId
            info.m_text = col.columnText
            self.InsertColumnInfo(i, info)
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER if col.size is wx.LIST_AUTOSIZE else col.size)
            i += 1

    def resizeChecker(self, event):
        if self.activeColumns[event.Column].resizable is False:
            event.Veto()

    def dragCheck(self, event):
        print event

    def dragEnd(self, event):
        print event
