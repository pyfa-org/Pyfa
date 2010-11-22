import wx
import copy
from gui import bitmapLoader
import gui.mainFrame
from gui.PFListPane import PFListPane
import service.fleet

from wx.lib.buttons import GenBitmapButton

FleetSelected, EVT_FLEET_SELECTED = wx.lib.newevent.NewEvent()

FleetItemSelect, EVT_FLEET_ITEM_SELECT = wx.lib.newevent.NewEvent()
FleetItemDelete, EVT_FLEET_ITEM_DELETE = wx.lib.newevent.NewEvent()
FleetItemNew, EVT_FLEET_ITEM_NEW = wx.lib.newevent.NewEvent()



class FleetBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.sFleet = service.fleet.Fleet.getInstance()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.hpane = FleetBrowserHeader(self)
        mainSizer.Add(self.hpane, 0, wx.EXPAND)

        self.m_sl2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_sl2, 0, wx.EXPAND, 0 )

        self.fleetItemContainer = PFFleetItemContainer(self)

        mainSizer.Add(self.fleetItemContainer, 1, wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)

        self.Bind(EVT_FLEET_ITEM_NEW, self.AddNewFleetItem)
        self.Bind(EVT_FLEET_ITEM_SELECT, self.SelectFleetItem)

        self.PopulateFleetList()

    def AddNewFleetItem(self, event):
        fleetName = event.fleetName
        newFleet = self.sFleet.addFleet()
        self.sFleet.renameFleet(newFleet, fleetName)

        self.fleetItemContainer.AddWidget(FleetItem(self, newFleet.ID, newFleet.name, newFleet.count()))
        self.fleetItemContainer.RefreshList()

    def SelectFleetItem(self, event):
        fleetID = event.fleetID
        self.fleetItemContainer.SelectWidgetByFleetID(fleetID)
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=fleetID))

    def PopulateFleetList(self, filter = ""):
        self.Freeze()
        self.fleetItemContainer.RemoveAllChildren()
        fleetList = self.sFleet.getFleetList()
        for fleetID, fleetName, fleetCount in fleetList:
            if fleetName.lower().find(filter.lower()) != -1:
                self.fleetItemContainer.AddWidget(FleetItem(self, fleetID, fleetName, fleetCount))
        self.fleetItemContainer.RefreshList()
        self.Thaw()

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
        self.Layout()
        self.fleetItemContainer.Layout()
        self.fleetItemContainer.RefreshList(True)
        event.Skip()


class FleetBrowserHeader (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 24), style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.newBmp = bitmapLoader.getBitmap("fit_add_small","icons")
        bmpSize = (16,16)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        if 'wxMac' in wx.PlatformInfo:
            bgcolour = wx.Colour(0, 0, 0, 0)
        else:
            bgcolour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE )

        self.fbNewFleet = PFGenBitmapButton( self, wx.ID_ANY, self.newBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE )
        mainSizer.Add(self.fbNewFleet, 0, wx.LEFT | wx.TOP | wx.BOTTOM  | wx.ALIGN_CENTER_VERTICAL , 5)
        self.fbNewFleet.SetBackgroundColour( bgcolour )

        self.sl1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        mainSizer.Add( self.sl1, 0, wx.EXPAND |wx.LEFT, 5 )

        self.tcFilter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        mainSizer.Add( self.tcFilter, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.stStatus = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stStatus.Wrap( -1 )
        mainSizer.Add( self.stStatus, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.SetSizer(mainSizer)
        self.Layout()

        self.fbNewFleet.Bind(wx.EVT_ENTER_WINDOW, self.fbNewEnterWindow)
        self.fbNewFleet.Bind(wx.EVT_LEAVE_WINDOW, self.fbHItemLeaveWindow)
        self.fbNewFleet.Bind(wx.EVT_BUTTON, self.OnNewFleetItem)

        self.tcFilter.Bind(wx.EVT_TEXT, self.OnFilterText)

        self.tcFilter.Bind(wx.EVT_ENTER_WINDOW, self.fbFilterEnterWindow)
        self.tcFilter.Bind(wx.EVT_LEAVE_WINDOW, self.fbHItemLeaveWindow)

    def OnFilterText(self, event):
        filter = self.tcFilter.GetValue()
        self.Parent.PopulateFleetList(filter)
        event.Skip()

    def OnNewFleetItem(self, event):
        wx.PostEvent(self.Parent, FleetItemNew(fleetName = "New Fleet"))

    def fbNewEnterWindow(self, event):
        self.stStatus.SetLabel("New fleet")
        event.Skip()

    def fbHItemLeaveWindow(self, event):
        self.stStatus.SetLabel("")
        event.Skip()

    def fbFilterEnterWindow(self, event):
        self.stStatus.SetLabel("Filter list")
        event.Skip()



class PFFleetItemContainer(PFListPane):
    def __init__(self,parent):
        PFListPane.__init__(self,parent)
        self.selectedWidget = -1

    def IsWidgetSelectedByContext(self, widget):
        if self.GetWidgetList()[widget].IsSelected():
            return True
        return False

    def GetWidgetIndex(self, widgetWnd):
        return self.GetWidgetList().index(widgetWnd)

    def GetWidgetByFleetID(self, fleetID):
        for widget in self.GetWidgetList():
            if widget.fleetID == fleetID:
                return widget
        return None

    def SelectWidget(self, widgetWnd):
        wlist = self.GetWidgetList()
        if self.selectedWidget != -1:
            wlist[self.selectedWidget].SetSelected(False)
            wlist[self.selectedWidget].Refresh()
        windex = self.GetWidgetIndex(widgetWnd)
        wlist[windex].SetSelected(True)
        wlist[windex].Refresh()
        self.selectedWidget = windex

    def SelectWidgetByFleetID(self, fleetID):
        widgetWnd = self.GetWidgetByFleetID(fleetID)
        if widgetWnd:
            self.SelectWidget(widgetWnd)

    def RemoveWidget(self, child):
        child.Destroy()
        self.selectedWidget = -1
        self._wList.remove(child)


    def RemoveAllChildren(self):
        for widget in self._wList:
            widget.Destroy()

        self.selectedWidget = -1
        self._wList = []


class FleetItem(wx.Window):
    def __init__(self, parent, fleetID, fleetName, fleetCount,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0,32), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

#        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
#        self.fleetBrowser = self.mainFrame.fleetBrowser
#        print self.fleetBrowser
        self.fleetID = fleetID
        self.fleetName = fleetName
        self.fleetCount = fleetCount
        self.highlighted = 0
        self.selected = False
        self.padding = 5
        self.fontBig = wx.FontFromPixelSize((0,15),wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.fontSmall = wx.FontFromPixelSize((0,13),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.copyBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.renameBmp = bitmapLoader.getBitmap("fit_rename_small", "icons")
        self.deleteBmp = bitmapLoader.getBitmap("fit_delete_small","icons")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)

        self.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.EnterWindow)
        self.Bind(wx.EVT_LEFT_UP, self.OnSelect)

    def OnSelect(self, event):
#        self.Parent.SelectWidget(self)
        wx.PostEvent(self.Parent.Parent, FleetItemSelect(fleetID = self.fleetID))
        event.Skip()

    def Rename(self, newName):
        self.fleetName = newName

    def Delete(self):
        print "Delete stuff..."

    def Copy(self):
        print "Copy"

    def IsSelected(self):
        return self.selected

    def SetSelected(self, state = True):
        self.selected = state

    def OnPaint(self, event):
        rect = self.GetRect()

        #Bitmap for our buffered DC
        canvas = wx.EmptyBitmap(rect.width, rect.height)

        #Buffered DC
        bdc = wx.BufferedPaintDC(self)
        bdc.SelectObject(canvas)

        #gradient rect - clear the window
        grect = copy.copy(rect)
        grect.top = grect.left = 0

        grect.height = grect.height / 2

        if self.highlighted:

            sr = 221
            sg = 221
            sb = 221

            startColor = (sr,sg,sb)

            bdc.GradientFillLinear(grect, startColor, wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
            grect.top = grect.height
            bdc.GradientFillLinear(grect, startColor, wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
            bdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))

        else:
            if self.selected:
                bkcolor = wx.Colour(221,221,221)
            else:
                bkcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

            bdc.SetBackground(wx.Brush(bkcolor))
            bdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
            bdc.Clear()

        suffix = "%d ships" % self.fleetCount if self.fleetCount >1 else "%d ship" % self.fleetCount if self.fleetCount == 1 else "No ships"
        fleetCount = "Fleet size: %s" % suffix
        bdc.SetFont(self.fontBig)

        fnx,fny = bdc.GetTextExtent(self.fleetName)

        bdc.DrawText(self.fleetName, self.padding, (rect.height/2 - fny)/2)

        bdc.SetFont(self.fontSmall)
        fcx,fcy = bdc.GetTextExtent(fleetCount)

        bdc.DrawText(fleetCount, self.padding, rect.height/2 + (rect.height/2 -fcy) / 2 )

        self.deletePosX = rect.width - self.deleteBmp.GetWidth() - self.padding
        self.renamePosX = self.deletePosX - self.renameBmp.GetWidth() - self.padding
        self.copyPosX = self.renamePosX - self.copyBmp.GetWidth() - self.padding
        self.renamePosY = self.deletePosY = self.copyPosY = (rect.height - self.renameBmp.GetHeight()) / 2

        bdc.DrawBitmap(self.copyBmp, self.copyPosX, self.copyPosY, 0)
        bdc.DrawBitmap(self.renameBmp, self.renamePosX, self.renamePosY, 0)
        bdc.DrawBitmap(self.deleteBmp, self.deletePosX, self.deletePosY, 0)

    def EnterWindow(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def LeaveWindow(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()


class PFGenBitmapButton(GenBitmapButton):
    def __init__(self, parent, id, bitmap, pos, size, style):
        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style)
        self.bgcolor = wx.Brush(wx.WHITE)

    def SetBackgroundColour(self, color):
        self.bgcolor = wx.Brush(color)

    def GetBackgroundBrush(self, dc):
        return self.bgcolor