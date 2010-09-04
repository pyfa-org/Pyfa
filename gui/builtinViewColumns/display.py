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

import wx
import gui.mainFrame

class Display(wx.ListCtrl):
    def __init__(self, parent):
        from gui.builtinViewColumns import *
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.BORDER_NONE)

        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        self.activeColumns = []
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.resizeChecker)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        i = 0
        for colName in self.DEFAULT_COLS:
            if colName[0:5] == "attr:":
                attrName = colName[5:]
                params = {"showIcon": True,
                          "displayName": False,
                          "attribute": attrName}
                col = gui.builtinViewColumns.getColumn("Attribute Display")(self, params)
            else:
                col = gui.builtinViewColumns.getColumn(colName)(self, None)

            self.addColumn(i, col)
            i += 1

        self.imageListBase = self.imageList.ImageCount

    def OnEraseBackGround(self, event):
        #Prevent flicker by not letting the parent's method get called.
        pass

    def addColumn(self, i, col):
        self.activeColumns.append(col)
        info = wx.ListItem()
        info.m_mask = col.mask
        info.m_image = col.imageId
        info.m_text = col.columnText
        self.InsertColumnInfo(i, info)
        col.resized = False
        self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER if col.size is wx.LIST_AUTOSIZE else col.size)

    def resizeChecker(self, event):
        if self.activeColumns[event.Column].resizable is False:
            event.Veto()
        else:
            self.activeColumns[event.Column].resized = True

    def clearItemImages(self):
        for i in xrange(self.imageList.ImageCount - 1, self.imageListBase, -1):
            self.imageList.Remove(i)
