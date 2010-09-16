# -*- coding: utf-8 -*-

###########################################################################
## pyfatogllepanel.py
##
## Author: Darriele - HomeWorld
## Serial: 2010090702  (YYYYMMDDII)
## Project home: http://www.evefit.org - pyfa project
##               http://www.evefit.org is the home for pyfa / eos  / aurora
## Some portions of code are based on
## AGW:pycollapsiblepane generic implementation of wx.CollapsiblePane
## AGW:pycollapsiblepane credits ( from the original source file used ):
##      Andrea Gavana, @ 09 Aug 2007
##      Latest Revision: 12 Apr 2010, 12.00 GMT
##
## Module description:
##      TogglePanel class is a wx.collipsablepane like implementation that uses
##      some optimization from awg::pycollipsablepane to provide certain
##      features tailored for PYFA needs.
##
## This module is part of PYFA (PYthon Fitting Assitant) and it shares the same
## licence ( read PYFA licence notice: gpl.txt )
###########################################################################

import wx
from gui import bitmapLoader

###########################################################################
## Class TogglePanel
###########################################################################

class TogglePanel ( wx.Panel ):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
        self.InheritAttributes()
        self._toggle = 1
        self.parent = parent

        self.bkColour = self.GetBackgroundColour()

#       Odd stuff :S
#        self.SetBackgroundColour( self.bkColour )

#       Create the main sizer of this panel

        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( self.mainSizer )
        parentSize = parent.GetMinSize()

#       Create the header panel

        self.headerPanel = wx.Panel(self)
        self.headerPanel.InheritAttributes()
#        self.headerPanel.SetBackgroundColour( self.bkColour)

        self.mainSizer.Add(self.headerPanel,0,wx.EXPAND | wx.TOP|wx.BOTTOM|wx.RIGHT, 1)

#       Attempt to use native treeitembitmaps - fails on some linux distros / w.mangers
#		self.bmpExpanded = self.GetNativeTreeItemBitmap("expanded")
#		self.bmpCollapsed =  self.GetNativeTreeItemBitmap("")
#

#       Load expanded/collapsed bitmaps from the icons folder

        self.bmpExpanded = bitmapLoader.getBitmap("down-arrow2","icons")
        self.bmpCollapsed = bitmapLoader.getBitmap("up-arrow2","icons")

#       Make the bitmaps have the same color as window text

        sysTextColour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )

        img = self.bmpExpanded.ConvertToImage()
        img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
        self.bmpExpanded = wx.BitmapFromImage(img)

        img = self.bmpCollapsed.ConvertToImage()
        img.Replace(0, 0, 0, sysTextColour[0], sysTextColour[1], sysTextColour[2])
        self.bmpCollapsed = wx.BitmapFromImage(img)

#       Assign the bitmaps to the header static bitmap control

        self.headerBmp = wx.StaticBitmap(self.headerPanel )
        self.headerBmp.SetBitmap( self.bmpExpanded)

#       Create the header sizer and append the static bitmap and static text controls

        headerSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.headerPanel.SetSizer( headerSizer)

        hbmpSizer = wx.BoxSizer( wx.HORIZONTAL )
        hlblSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.hcntSizer = wx.BoxSizer( wx.HORIZONTAL)

        hbmpSizer.Add( self.headerBmp, 0,0, 5 )

        self.headerLabel = wx.StaticText( self.headerPanel, wx.ID_ANY, u"PYFA", wx.DefaultPosition, wx.DefaultSize, 0 )
        hlblSizer.Add( self.headerLabel, 0, wx.EXPAND , 5 )

        headerSizer.Add( hbmpSizer, 0,  wx.RIGHT, 5 )
        headerSizer.Add( hlblSizer, 0, wx.RIGHT, 5 )
        headerSizer.Add( self.hcntSizer, 0, wx.RIGHT, 5)

#       Set the static text font weight to BOLD

        headerFont=parent.GetFont()
        headerFont.SetWeight(wx.BOLD)
        self.headerLabel.SetFont(headerFont)

#       Create the content panel and its main sizer


        self.contentSizer = wx.BoxSizer( wx.VERTICAL )
        self.contentPanel = wx.Panel(self)
        self.contentPanel.InheritAttributes()
        self.contentPanel.SetSizer(self.contentSizer)

        self.mainSizer.Add( self.contentPanel, 0, wx.EXPAND | wx.RIGHT | wx.LEFT , 5)


        self.Layout()



        # Connect Events
        self.headerLabel.Bind( wx.EVT_LEFT_UP, self.toggleContent )
        self.headerBmp.Bind( wx.EVT_LEFT_UP, self.toggleContent )
        self.headerPanel.Bind( wx.EVT_LEFT_UP, self.toggleContent )
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.headerPanel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.contentPanel.Bind(wx.EVT_PAINT, self.OnPaint)


    def __del__( self ):
        pass

    def OnPaint(self, event):
        self.contentPanel.Layout()
        self.headerPanel.Layout()
        event.Skip()

    def AddToggleItem(self, hitem):
        hitem.Bind( wx.EVT_LEFT_UP, self.toggleContent )

    def GetHeaderContentSizer(self):
        return self.hcntSizer

    def GetHeaderPanel(self):
        return self.headerPanel
    def InsertItemInHeader(self, item):
        self.hcntSizer.Add(item,0,0,0)
        self.Layout()
    def AddSizer(self, sizer):
        self.contentSizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 0)
        self.Layout()

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

    def IsCollapsed(self):
        """ Returns ``True`` if the pane window is currently hidden. """
        if self._toggle == 1:
            return False
        else:
            return True


    def IsExpanded(self):
        """ Returns ``True`` if the pane window is currently shown. """
        if self._toggle == 1:
            return False
        else:
            return True


    def OnStateChange(self, sz):
        """
        Handles the status changes (collapsing/expanding).

        :param `sz`: an instance of `wx.Size`.
        """

        # minimal size has priority over the best size so set here our min size
        self.SetMinSize(sz)
        self.SetSize(sz)

        self.parent.GetSizer().SetSizeHints(self.parent)


        if self.IsCollapsed():
                # expanded . collapsed transition
            if self.parent.GetSizer():
                # we have just set the size hints...
                sz = self.parent.GetSizer().CalcMin()

                # use SetClientSize() and not SetSize() otherwise the size for
                # e.g. a wxFrame with a menubar wouldn't be correctly set
                self.parent.SetClientSize(sz)

            else:
                self.parent.Layout()

        else:

                    # collapsed . expanded transition

                    # force our parent to "fit", i.e. expand so that it can honour
                    # our minimal size
            self.parent.Fit()





    # Toggle the content panel (hide/show)

    def toggleContent( self, event ):
        self.Freeze()
        if self._toggle == 1:
#            self.contentPanel.Hide()
            self.contentMinSize = self.contentPanel.GetSize()
            self.contentPanel.SetMinSize(wx.Size(self.contentMinSize[0],0))
            self.headerBmp.SetBitmap( self.bmpCollapsed)


        else:
#            self.contentPanel.Show()
            self.contentPanel.SetMinSize(self.contentMinSize)

            self.headerBmp.SetBitmap( self.bmpExpanded)


        self._toggle *=-1

        self.Thaw()
        self.OnStateChange(self.GetBestSize())

#        self.parent.Layout()


    # Highlight stuff, not used for now

    def enterWindow( self, event ):

        self.headerPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.headerPanel.Refresh()

        event.Skip()

    def leaveWindow( self, event ):

        self.headerPanel.SetBackgroundColour( self.bkColour )
        self.headerPanel.Refresh()

        event.Skip()

