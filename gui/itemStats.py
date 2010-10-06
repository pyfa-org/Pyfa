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
import wx.gizmos
import gui.mainFrame
import bitmapLoader
import sys

from util import formatAmount

class ItemStatsDialog(wx.Dialog):
    counter = 0
    def __init__(self, victim):
        wx.Dialog.__init__(self,
                          gui.mainFrame.MainFrame.getInstance(),
                          wx.ID_ANY, title="Item stats",
                          #style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)
                          style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU )

        empty = getattr(victim, "isEmpty", False)
        if empty:
            self.Hide()
            self.Destroy()
            return

        item = getattr(victim, "item", None)
        if item is None:
            item = victim
            victim = None

        if item.icon is not None:
            self.SetIcon(wx.IconFromBitmap(bitmapLoader.getBitmap(item.icon.iconFile, "pack")))
        self.SetTitle("Item Stats: %s" % item.name)

        self.SetMinSize((500, 300))
        self.SetSize((500, 300))
        self.SetMaxSize((500, 300))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.container = ItemStatsContainer(self, victim, item)
        self.mainSizer.Add(self.container, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        parent = gui.mainFrame.MainFrame.getInstance()

        dlgsize = self.GetSize()
        psize = parent.GetSize()
        ppos = parent.GetPosition()
        ItemStatsDialog.counter += 1
        counter = ItemStatsDialog.counter
        dlgStep = 30
        if counter * dlgStep > ppos.x+psize.width-dlgsize.x or counter * dlgStep > ppos.y+psize.height-dlgsize.y:
            ItemStatsDialog.counter = 1

        dlgx = ppos.x + counter * dlgStep
        dlgy = ppos.y + counter * dlgStep
        self.SetPosition((dlgx,dlgy))

        self.Show()

        self.Bind(wx.EVT_CLOSE, self.closeEvent)

    def closeEvent(self, event):
        self.Destroy()
        event.Skip()

###########################################################################
## Class ItemStatsContainer
###########################################################################

class ItemStatsContainer ( wx.Panel ):

    def __init__( self, parent, stuff, item):
        wx.Panel.__init__ ( self, parent )
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.nbContainer = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.nbContainer, 1, wx.EXPAND |wx.ALL, 2 )

        self.desc = ItemDescription(self.nbContainer, stuff, item)
        self.params = ItemParams(self.nbContainer, stuff, item)
        self.reqs = ItemRequirements(self.nbContainer, stuff, item)
        self.effects = ItemEffects(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.desc, "Description")
        self.nbContainer.AddPage(self.params, "Attributes")
        self.nbContainer.AddPage(self.reqs, "Requirements")
        self.nbContainer.AddPage(self.effects, "Effects")

        self.SetSizer(mainSizer)
        self.Layout()

    def __del__( self ):
        pass


###########################################################################
## Class ItemDescription
###########################################################################

class ItemDescription ( wx.Panel ):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.description = wx.TextCtrl(self, wx.ID_ANY, item.description, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.NO_BORDER)
        mainSizer.Add(self.description, 1, wx.ALL|wx.EXPAND, 0)
        self.Layout()

###########################################################################
## Class ItemParams
###########################################################################

class ItemParams (wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.paramList = wx.ListCtrl(self, wx.ID_ANY,
                                     style = wx.LC_HRULES | wx.LC_NO_HEADER |wx.LC_REPORT |wx.LC_SINGLE_SEL |wx.LC_VRULES |wx.NO_BORDER)
        mainSizer.Add( self.paramList, 1, wx.ALL|wx.EXPAND, 0 )
        self.SetSizer( mainSizer )

        self.paramList.InsertColumn(0,"Attribute")
        self.paramList.InsertColumn(1,"Value")
        self.paramList.SetColumnWidth(0,300)
        self.paramList.SetColumnWidth(1,165)
        attrs = stuff.itemModifiedAttributes if stuff is not None else item.attributes
        names = list(attrs.iterkeys())
        names.sort()

        for name in names:
            index = self.paramList.InsertStringItem(sys.maxint, attrs[name].displayName.capitalize())
            self.paramList.SetStringItem(index, 1, str(attrs[name]) if stuff is not None else str(formatAmount(attrs[name].value, 3, 0, 0)))

        self.Layout()


###########################################################################
## Class ItemRequirements
###########################################################################

class ItemRequirements ( wx.Panel ):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent, style = wx.TAB_TRAVERSAL)

        #itemId is set by the parent.

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.reqTree = wx.gizmos.TreeListCtrl(self, style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)
        self.reqTree.AddColumn("Skill")
        self.reqTree.AddColumn("Level")
        self.reqTree.SetMainColumn(0)

        mainSizer.Add(self.reqTree, 1, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.root = self.reqTree.AddRoot("WINRARZOR")
        self.reqTree.SetPyData(self.root, None)

        self.imageList = wx.ImageList(16, 16)
        self.reqTree.SetImageList(self.imageList)
        skillBookId = self.imageList.Add(bitmapLoader.getBitmap("skill_small", "icons"))
        child = self.reqTree.AppendItem(self.root,"Requirements", skillBookId)
        for skill, level in item.requiredSkills.iteritems():
            item = self.reqTree.AppendItem(child, skill.name, skillBookId)
            self.reqTree.SetItemText(item, "%d" % level, 1)

        self.reqTree.ExpandAll(self.root)
        self.reqTree.SetColumnWidth(0, 420)
        self.reqTree.SetColumnWidth(1, 45)
        self.Layout()


###########################################################################
## Class ItemEffects
###########################################################################

class ItemEffects (wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__ (self, parent)
        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.effectList = wx.ListCtrl(self, wx.ID_ANY,
                                     style = wx.LC_HRULES |
                                      #wx.LC_NO_HEADER |
                                      wx.LC_REPORT |wx.LC_SINGLE_SEL |wx.LC_VRULES |wx.NO_BORDER)
        mainSizer.Add( self.effectList, 1, wx.ALL|wx.EXPAND, 0 )
        self.SetSizer( mainSizer )

        self.effectList.InsertColumn(0,"Name")
        self.effectList.InsertColumn(1,"Description")
        self.effectList.InsertColumn(2,"Implemented")
        self.effectList.SetColumnWidth(0,155)
        self.effectList.SetColumnWidth(1,235)
        self.effectList.SetColumnWidth(2,90)
        effects = item.effects
        names = list(effects.iterkeys())
        names.sort()

        for name in names:
            index = self.effectList.InsertStringItem(sys.maxint, name)
            self.effectList.SetStringItem(index, 1, str(effects[name].description))
            if effects[name].isImplemented:
                implemented = "Yes"
            else:
                implemented = "No"
            self.effectList.SetStringItem(index, 2, implemented)
        self.Layout()
