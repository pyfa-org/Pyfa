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
import bitmapLoader

class ItemStatsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,
                          gui.mainFrame.MainFrame.getInstance(),
                          wx.ID_ANY, title="pyfa - Item Stats",
                          #style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)
                          style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU )

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("pyfa", "icons"))
        self.SetIcon(i)

        self.SetMinSize((500, 300))
        self.SetSize((500, 300))
        self.SetMaxSize((500, 300))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.container = ItemStatsContainer(self)
        self.mainSizer.Add(self.container, 1, wx.EXPAND)
        self.SetSizer(self.mainSizer)
        self.Show()

class ItemStatsMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

        self.showInfoId = wx.NewId()
        self.Append(self.showInfoId, "&Item stats", "moo")
        self.Bind(wx.EVT_MENU, self.itemStats, id=self.showInfoId)

    def setItem(self, itemId):
        self.itemId = itemId

    def itemStats(self, event):
        ItemStatsFrame()


###########################################################################
## Class ItemStatsContainer
###########################################################################

class ItemStatsContainer ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.nbContainer = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        mainSizer.Add( self.nbContainer, 1, wx.EXPAND |wx.ALL, 2 )

        self.desc = ItemDescription(self.nbContainer)
        self.params = ItemParams(self.nbContainer)
        self.reqs = ItemRequirements(self.nbContainer)
        self.nbContainer.AddPage(self.desc, "Description")
        self.nbContainer.AddPage(self.params, "Attributes")
        self.nbContainer.AddPage(self.reqs, "Requirements")
        
        self.SetSizer( mainSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class ItemDescription
###########################################################################

class ItemDescription ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.description = wx.StaticText( self, wx.ID_ANY, u"None", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.description.Wrap( -1 )
        mainSizer.Add( self.description, 1, wx.ALL|wx.EXPAND, 2 )
        
        self.SetSizer( mainSizer )
        self.Layout()
    
    def __del__( self ):
        pass


###########################################################################
## Class ItemParams
###########################################################################

class ItemParams ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.paramList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES
                                      |wx.LC_NO_HEADER
                                      |wx.LC_REPORT
                                      |wx.LC_SINGLE_SEL
                                      |wx.LC_VRULES )
        mainSizer.Add( self.paramList, 1, wx.ALL|wx.EXPAND, 2 )
        
        self.SetSizer( mainSizer )
        self.Layout()
    
    def __del__( self ):
        pass
	

###########################################################################
## Class ItemRequirements
###########################################################################

class ItemRequirements ( wx.Panel ):
	
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.reqTree = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
        mainSizer.Add( self.reqTree, 1, wx.ALL|wx.EXPAND, 2 )
        
        self.SetSizer( mainSizer )
        self.Layout()

    def __del__( self ):
        pass
    

