# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May  4 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
from gui import bitmapLoader
###########################################################################
## Class TogglePanel
###########################################################################

class TogglePanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )

		self._toggle = 1
                self.parent = parent
                
		self.bmpExpanded = self.GetNativeTreeItemBitmap("expanded")
		self.bmpCollapsed =  self.GetNativeTreeItemBitmap("")
		
		self.headerBmp = wx.StaticBitmap(self)
                self.headerBmp.SetBitmap( self.bmpExpanded)
                
		self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		
		headerSizer = wx.BoxSizer( wx.HORIZONTAL )
		headerSizer.Add( self.headerBmp, 0, wx.TOP|wx.BOTTOM | wx.LEFT, 5 )
		
		self.paneLabel = wx.StaticText( self, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		headerSizer.Add( self.paneLabel, 1, wx.EXPAND | wx.TOP|wx.BOTTOM | wx.RIGHT, 5 )


		headerFont=parent.GetFont()
		headerFont.SetWeight(wx.BOLD)
		self.paneLabel.SetFont(headerFont)
		
        	self.mainSizer.Add( headerSizer, 0, wx.EXPAND, 5 )
		
		self.contentSizer = wx.BoxSizer( wx.VERTICAL )
		self.contentPanel = wx.Panel(self)
		self.contentPanel.SetSizer(self.contentSizer)
		
                self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
                
		self.mainSizer.Add( self.contentPanel, 1, wx.EXPAND, 5)
		self.SetSizer( self.mainSizer )

                self.paneLabel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
                self.headerBmp.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )		

		self.Layout()
		
		# Connect Events
		self.paneLabel.Bind( wx.EVT_LEFT_UP, self.toggleContent )
		self.headerBmp.Bind( wx.EVT_LEFT_UP, self.toggleContent )
#		self.paneLabel.Bind( wx.EVT_ENTER_WINDOW, self.enterWindow )
#		self.paneLabel.Bind( wx.EVT_LEAVE_WINDOW, self.leaveWindow )
#		self.headerBmp.Bind( wx.EVT_ENTER_WINDOW, self.enterWindow )
#		self.headerBmp.Bind( wx.EVT_LEAVE_WINDOW, self.leaveWindow )		
	
	def __del__( self ):
		pass
	
	def AddSizer(self, sizer):
       		self.contentSizer.Add(sizer, 1, wx.EXPAND, 5)
                self.Fit()
                
	def GetContentPane(self):
                return self.contentPanel
        
        def SetLabel(self, label):
                self.paneLabel.SetLabel(label)
                
        def GetNativeTreeItemBitmap(self, mode):
                
                bitmap = wx.EmptyBitmap(18, 18)
                dc = wx.MemoryDC()
                dc.SelectObject(bitmap)
                dc.SetBackground(wx.TheBrushList.FindOrCreateBrush(wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ), wx.SOLID))
                dc.Clear()

                wx.RendererNative.Get().DrawTreeItemButton(self, dc, wx.Rect(0, 0, 18, 18), wx.CONTROL_EXPANDED if mode == "expanded" else 0)

                dc.Destroy()
                
	        return bitmap        
                
	# Virtual event handlers, overide them in your derived class
	def toggleContent( self, event ):
                if self._toggle == 1:
                        self.contentPanel.Hide()
                        self.headerBmp.SetBitmap( self.bmpCollapsed)
                else:
                        self.contentPanel.Show()
                        self.headerBmp.SetBitmap( self.bmpExpanded)
                self._toggle *=-1
                self.parent.Layout()
		event.Skip()
	
	def enterWindow( self, event ):

                self.paneLabel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
                self.headerBmp.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )

                self.headerBmp.Refresh()
                self.paneLabel.Refresh()

		event.Skip()
	
	def leaveWindow( self, event ):

                self.paneLabel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
                self.headerBmp.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

                self.headerBmp.Refresh()                
                self.paneLabel.Refresh()

		event.Skip()
	
