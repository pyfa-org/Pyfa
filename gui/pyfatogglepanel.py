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
                
                self.mainSizer = wx.BoxSizer( wx.VERTICAL )
		self.SetSizer( self.mainSizer )

		self.headerPanel = wx.Panel(self)
#                self.headerPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT) )

                self.mainSizer.Add(self.headerPanel,0,wx.EXPAND,5)

		
#		self.bmpExpanded = self.GetNativeTreeItemBitmap("expanded")
#		self.bmpCollapsed =  self.GetNativeTreeItemBitmap("")

                self.bmpExpanded = bitmapLoader.getBitmap("up-arrow2","icons")
		self.bmpCollapsed = bitmapLoader.getBitmap("down-arrow2","icons")

		sysTextColour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )

                img = self.bmpExpanded.ConvertToImage()
                img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
                self.bmpExpanded = wx.BitmapFromImage(img)
                
                img = self.bmpCollapsed.ConvertToImage()
                img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
                self.bmpCollapsed = wx.BitmapFromImage(img)
		
		self.headerBmp = wx.StaticBitmap(self.headerPanel )
                self.headerBmp.SetBitmap( self.bmpExpanded)
              
		
		headerSizer = wx.BoxSizer( wx.HORIZONTAL )
        	self.headerPanel.SetSizer( headerSizer)
        	
		hbmpSizer = wx.BoxSizer( wx.VERTICAL )
		hlblSizer = wx.BoxSizer( wx.VERTICAL )
		
		hbmpSizer.Add( self.headerBmp, 0,0, 5 )
		
		self.headerLabel = wx.StaticText( self.headerPanel, wx.ID_ANY, u"Test", wx.DefaultPosition, wx.DefaultSize, 0 )
		hlblSizer.Add( self.headerLabel, 1, wx.EXPAND , 5 )

                headerSizer.Add( hbmpSizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5 )
                headerSizer.Add( hlblSizer, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		headerFont=parent.GetFont()
		headerFont.SetWeight(wx.BOLD)
		self.headerLabel.SetFont(headerFont)

		
		self.contentSizer = wx.BoxSizer( wx.VERTICAL )
		self.contentPanel = wx.Panel(self)
		self.contentPanel.SetSizer(self.contentSizer)
		
#                self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
                
		self.mainSizer.Add( self.contentPanel, 1, wx.EXPAND, 5)


		self.Layout()
		
		# Connect Events
		self.headerLabel.Bind( wx.EVT_LEFT_UP, self.toggleContent )
		self.headerBmp.Bind( wx.EVT_LEFT_UP, self.toggleContent )
		self.headerPanel.Bind( wx.EVT_LEFT_UP, self.toggleContent )
		
		self.headerLabel.Bind( wx.EVT_ENTER_WINDOW, self.enterWindow )
		self.headerLabel.Bind( wx.EVT_LEAVE_WINDOW, self.leaveWindow )
		self.headerBmp.Bind( wx.EVT_ENTER_WINDOW, self.enterWindow )
		self.headerBmp.Bind( wx.EVT_LEAVE_WINDOW, self.leaveWindow )		

		self.headerPanel.Bind( wx.EVT_ENTER_WINDOW, self.enterWindow )
		self.headerPanel.Bind( wx.EVT_LEAVE_WINDOW, self.leaveWindow )		
	
	def __del__( self ):
		pass
	
	def AddSizer(self, sizer):
       		self.contentSizer.Add(sizer, 1, wx.EXPAND, 5)
                self.Fit()
                
	def GetContentPane(self):
                return self.contentPanel
        
        def SetLabel(self, label):
                self.headerLabel.SetLabel(label)
                
        def GetNativeTreeItemBitmap(self, mode):
                
                bitmap = wx.EmptyBitmap(24, 24)
                dc = wx.MemoryDC()
                dc.SelectObject(bitmap)
                dc.SetBackground(wx.TheBrushList.FindOrCreateBrush(self.parent.GetBackgroundColour(), wx.SOLID))
                dc.Clear()

                wx.RendererNative.Get().DrawTreeItemButton(self, dc, wx.Rect(0, 0, 24, 24), wx.CONTROL_EXPANDED if mode == "expanded" else 0)

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

                self.headerPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
                self.headerPanel.Refresh()
                pass
		event.Skip()
	
	def leaveWindow( self, event ):

                self.headerPanel.SetBackgroundColour( self.parent.GetBackgroundColour() )
                self.headerPanel.Refresh()                

                pass
		event.Skip()
	
