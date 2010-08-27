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
import controller
import gui.builtinViewColumns
import gui.shipBrowser as sb
import gui.mainFrame
from gui.builtinViewColumns import *
import sys

class FittingView(wx.ListCtrl):
    DEFAULT_COLS = ["Module state",
                    "Module name/slot",
                    "attr:power",
                    "attr:cpu",
                    "attr:capacitorNeed",
                    "attr:trackingSpeed",
                    "Max range"]

    def __init__(self, parent):
        listStyle = wx.LC_REPORT | wx.BORDER_NONE
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=listStyle)

        self.imageList = wx.ImageList(16, 16)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        self.activeColumns = []
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.resizeChecker)

        mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.shipBrowser = mainFrame.shipBrowser
        self.shipView = mainFrame.shipBrowser.shipView
        self.searchView = mainFrame.shipBrowser.shipView
        self.switch = mainFrame.fitMultiSwitch

        i = 0
        for colName in FittingView.DEFAULT_COLS:
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
        self.activeFitID = None
        self.Hide() #Don't show ourselves at start

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
        for i in xrange(self.imageList.ImageCount, self.imageListBase, -1):
            self.imageList.Remove(i)

    #Gets called from the fitMultiSwitch when it decides its time
    def changeFit(self, fitID):
        self.activeFitID = fitID
        if fitID == None:
            self.Hide()
        else:
            cFit = controller.Fit.getInstance()
            fit = cFit.getFit(fitID)
            self.DeleteAllItems()
            self.clearItemImages()
            for mod in fit.modules:
                index = self.InsertStringItem(sys.maxint, "")
                for i, col in enumerate(self.activeColumns):
                    self.SetStringItem(index, i, col.getText(mod), col.getImageId(mod))

            for i, col in enumerate(self.activeColumns):
                if not col.resized:
                    self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
                    if self.GetColumnWidth(i) < 40:
                        self.SetColumnWidth(i, 40)
            self.Show()
