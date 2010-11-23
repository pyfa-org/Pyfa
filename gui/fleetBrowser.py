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
FleetItemCopy, EVT_FLEET_ITEM_COPY = wx.lib.newevent.NewEvent()
FleetItemRename, EVT_FLEET_ITEM_RENAME = wx.lib.newevent.NewEvent()



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

        self.filter = ""

        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)

        self.Bind(EVT_FLEET_ITEM_NEW, self.AddNewFleetItem)
        self.Bind(EVT_FLEET_ITEM_SELECT, self.SelectFleetItem)
        self.Bind(EVT_FLEET_ITEM_DELETE, self.DeleteFleetItem)
        self.Bind(EVT_FLEET_ITEM_COPY, self.CopyFleetItem)
        self.Bind(EVT_FLEET_ITEM_RENAME, self.RenameFleetItem)

        self.PopulateFleetList()

    def AddNewFleetItem(self, event):
        fleetName = event.fleetName
        newFleet = self.sFleet.addFleet()
        self.sFleet.renameFleet(newFleet, fleetName)

        self.AddItem(newFleet.ID, newFleet.name, newFleet.count())

    def SelectFleetItem(self, event):
        fleetID = event.fleetID
        self.fleetItemContainer.SelectWidgetByFleetID(fleetID)
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=fleetID))

    def CopyFleetItem(self, event):
        fleetID = event.fleetID
        fleet = self.sFleet.copyFleetByID(fleetID)

        fleetName = fleet.name + " Copy"
        self.sFleet.renameFleet(fleet,fleetName)

        self.AddItem(fleet.ID, fleet.name, fleet.count())

        self.fleetItemContainer.SelectWidgetByFleetID(fleet.ID)
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=fleet.ID))

    def RenameFleetItem(self, event):
        fleetID = event.fleetID
        fleet = self.sFleet.getFleetByID(fleetID)

        newFleetName = event.fleetName

        self.sFleet.renameFleet(fleet, newFleetName)

    def DeleteFleetItem(self, event):
        self.sFleet.deleteFleetByID(event.fleetID)
        self.PopulateFleetList()

    def AddItem (self, ID, name, count):
        self.fleetItemContainer.AddWidget(FleetItem(self, ID, name, count))
        self.fleetItemContainer.RefreshList()

    def PopulateFleetList(self):
        self.Freeze()
        filter = self.filter
        self.fleetItemContainer.RemoveAllChildren()
        fleetList = self.sFleet.getFleetList()
        for fleetID, fleetName, fleetCount in fleetList:
            if fleetName.lower().find(filter.lower()) != -1:
                self.fleetItemContainer.AddWidget(FleetItem(self, fleetID, fleetName, fleetCount))
        self.fleetItemContainer.RefreshList()
        self.Thaw()

    def SetFilter(self, filter):
        self.filter = filter

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
        self.Parent.SetFilter(filter)
        self.Parent.PopulateFleetList()
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
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

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

    def OnLeftUp(self, event):
        event.Skip()

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

        self.buttonsTip = ""
        self.selected = False
        self.padding = 5
        self.editHasFocus = False

        self.cleanupTimer = None
        self.cleanupTimerId = wx.NewId()

        self.fontBig = wx.FontFromPixelSize((0,15),wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.fontSmall = wx.FontFromPixelSize((0,13),wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.copyBmp = bitmapLoader.getBitmap("fit_add_small", "icons")
        self.renameBmp = bitmapLoader.getBitmap("fit_rename_small", "icons")
        self.deleteBmp = bitmapLoader.getBitmap("fit_delete_small","icons")
        self.acceptBmp = bitmapLoader.getBitmap("faccept_small", "icons")

        self.copyBmpGrey = self.GreyBitmap(self.copyBmp)
        self.renameBmpGrey = self.GreyBitmap(self.renameBmp)
        self.deleteBmpGrey = self.GreyBitmap(self.deleteBmp)
        self.acceptBmpGrey = self.GreyBitmap(self.acceptBmp)

        self.btnSize = (18,18)

        if 'wxMac' in wx.PlatformInfo:
            self.btnbgcolour = wx.Colour(0, 0, 0, 0)
        else:
            self.btnbgcolour = wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DFACE)

        self.btnCopy = PFGenBitmapButton( self, wx.ID_ANY, self.copyBmp, wx.DefaultPosition, self.btnSize, wx.BORDER_NONE )
        self.btnCopy.Show(False)
        self.btnCopy.SetBackgroundColour( self.btnbgcolour )

        self.btnRename = PFGenBitmapButton( self, wx.ID_ANY, self.renameBmp, wx.DefaultPosition, self.btnSize, wx.BORDER_NONE )
        self.btnRename.Show(False)
        self.btnRename.SetBackgroundColour( self.btnbgcolour )

        self.btnDelete = PFGenBitmapButton( self, wx.ID_ANY, self.deleteBmp, wx.DefaultPosition, self.btnSize, wx.BORDER_NONE )
        self.btnDelete.Show(False)
        self.btnDelete.SetBackgroundColour( self.btnbgcolour )

        self.editWidth = 150
        self.tcFleetName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fleetName, wx.DefaultPosition, (self.editWidth,-1), wx.TE_PROCESS_ENTER)
        self.tcFleetName.Show(False)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)

        self.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.EnterWindow)
        self.Bind(wx.EVT_LEFT_UP, self.OnSelect)

        self.btnCopy.Bind(wx.EVT_ENTER_WINDOW, self.OnBtnEnterWindow)
        self.btnRename.Bind(wx.EVT_ENTER_WINDOW, self.OnBtnEnterWindow)
        self.btnDelete.Bind(wx.EVT_ENTER_WINDOW, self.OnBtnEnterWindow)

        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnDeleteBtn)
        self.btnCopy.Bind(wx.EVT_BUTTON, self.OnCopyBtn)
        self.btnRename.Bind(wx.EVT_BUTTON, self.OnRenameBtn)

        self.tcFleetName.Bind(wx.EVT_KILL_FOCUS, self.OnEditLostFocus)
        self.tcFleetName.Bind(wx.EVT_TEXT_ENTER, self.RenameFit)
        self.tcFleetName.Bind(wx.EVT_KEY_DOWN, self.EditCheckEsc)

        self.Bind(wx.EVT_TIMER, self.OnTimer)

    def OnSelect(self, event):
        if self.editHasFocus:
            self.HideEdit()
        else:
            wx.PostEvent(self.Parent.Parent, FleetItemSelect(fleetID = self.fleetID))
        event.Skip()

    def OnRenameBtn(self, event):
        if self.tcFleetName.IsShown():
            self.HideEdit()
            self.btnRename.SetBitmapLabel(self.renameBmp, False)
            self.RenameFit(None)
        else:
            if not self.editHasFocus:
                self.btnRename.SetBitmapLabel(self.acceptBmp,False)
                self.tcFleetName.Show(True)
                self.tcFleetName.SetFocus()
                self.tcFleetName.SelectAll()
                self.editHasFocus = True
        event.Skip()

    def OnDeleteBtn(self, event):
        if self.editHasFocus:
            self.HideEdit()
        else:
            wx.PostEvent(self.Parent.Parent, FleetItemDelete(fleetID = self.fleetID))
            event.Skip()

    def OnCopyBtn(self, event):
        if self.editHasFocus:
            self.HideEdit()
        else:
            wx.PostEvent(self.Parent.Parent, FleetItemCopy(fleetID = self.fleetID))
            event.Skip()

    def RenameFit(self, event):
        self.HideEdit()

        newFleetName = self.tcFleetName.GetValue()
        self.fleetName = newFleetName

        wx.PostEvent(self.Parent.Parent, FleetItemRename(fleetID = self.fleetID, fleetName = self.fleetName))
        self.Refresh()

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
        btnWidth,btnHeight = self.btnSize
        self.deletePosX = rect.width - btnWidth - self.padding
        self.renamePosX = self.deletePosX - btnWidth
        # - self.padding
        self.copyPosX = self.renamePosX - btnWidth
        # - self.padding
        self.renamePosY = self.deletePosY = self.copyPosY = (rect.height - btnHeight) / 2

        if self.highlighted:
            brush = wx.Brush(self.btnbgcolour)
            pen = wx.Pen(self.btnbgcolour)

            bdc.SetPen(pen)
            bdc.SetBrush(brush)

            tx,ty = bdc.GetTextExtent(self.buttonsTip)

            bdc.DrawRoundedRectangle(self.copyPosX - 8 - tx - self.padding, self.copyPosY-1, rect.width,20, 8)
            bdc.DrawText(self.buttonsTip,self.copyPosX - tx - self.padding, self.copyPosY + 8 - ty/2)

            self.btnCopy.SetPosition((self.copyPosX, self.copyPosY))
            self.btnRename.SetPosition((self.renamePosX, self.renamePosY))
            self.btnDelete.SetPosition((self.deletePosX, self.deletePosY))

            self.btnCopy.Show()
            self.btnRename.Show()
            self.btnDelete.Show()

        else:
            self.btnCopy.Show(False)
            self.btnRename.Show(False)
            self.btnDelete.Show(False)
            bdc.DrawBitmap(self.copyBmpGrey, self.copyPosX + 1, self.copyPosY + 1 )
            if self.editHasFocus:
                bdc.DrawBitmap(self.acceptBmpGrey, self.renamePosX + 1, self.renamePosY + 1 )
            else:
                bdc.DrawBitmap(self.renameBmpGrey, self.renamePosX + 1, self.renamePosY + 1 )
            bdc.DrawBitmap(self.deleteBmpGrey, self.deletePosX + 1, self.deletePosY + 1 )

        textStart = self.padding
        self.AdjustFleetNameEditSize(textStart, self.copyPosX - self.editWidth - self.padding)

    def AdjustFleetNameEditSize(self, start,end):
        if self.tcFleetName.IsShown():
            fnEditSize = self.tcFleetName.GetSize()
            wSize = self.GetSize()
            fnEditPosX = end
            fnEditPosY = (wSize.height - fnEditSize.height)/2
            if fnEditPosX < start:
                self.tcFleetName.SetSize((self.editWidth + fnEditPosX - start,-1))
                self.tcFleetName.SetPosition((start,fnEditPosY))
            else:
                self.tcFleetName.SetSize((self.editWidth,-1))
                self.tcFleetName.SetPosition((fnEditPosX,fnEditPosY))


    def OnEditLostFocus(self, event):
        if self.highlighted == 1:
            self.editHasFocus = True
        else:
            self.HideEdit()
        event.Skip()

    def EditCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.HideEdit()
        else:
            event.Skip()

    def HideEdit(self):
        self.tcFleetName.Show(False)
        self.editHasFocus = False
        self.btnRename.SetBitmapLabel(self.renameBmp, False)
        self.Refresh()


    def OnBtnEnterWindow(self, event):
        btn = event.GetEventObject()
        if btn == self.btnCopy:
            self.buttonsTip = "Copy Fleet"
        elif btn == self.btnDelete:
            self.buttonsTip = "Delete Fleet"
        elif btn == self.btnRename:
            self.buttonsTip = "Rename Fleet"
        else:
            self.buttonsTip = ""
        self.Refresh()
        event.Skip()


    def EnterWindow(self, event):
        if not self.cleanupTimer:
            self.cleanupTimer = wx.Timer(self, self.cleanupTimerId)
        if not self.cleanupTimer.IsRunning():
            self.cleanupTimer.Start(50)

        self.highlighted = 1
        self.buttonsTip = ""
        self.Refresh()
        event.Skip()

    def LeaveWindow(self, event):
        mposx, mposy = wx.GetMousePosition()
        rect = self.GetRect()
        rect.top = rect.left = 0
        cx,cy = self.ScreenToClient((mposx,mposy))
        if not rect.Contains((cx,cy)):
            self.highlighted = 0
            self.Refresh()
            if self.cleanupTimer:
                if self.cleanupTimer.IsRunning():
                    self.cleanupTimer.Stop()

        event.Skip()

    def OnTimer(self, event):
        if event.GetId() == self.cleanupTimerId:
            mposx, mposy = wx.GetMousePosition()
            rect = self.GetRect()
            rect.top = rect.left = 0
            cx,cy = self.ScreenToClient((mposx,mposy))
            if not rect.Contains((cx,cy)):
                self.highlighted = 0
                self.Refresh()
                self.cleanupTimer.Stop()
        event.Skip()

    def GreyBitmap(self, bitmap):
        img = bitmap.ConvertToImage()
        img = img.ConvertToGreyscale()
        return wx.BitmapFromImage(img)

class PFGenBitmapButton(GenBitmapButton):
    def __init__(self, parent, id, bitmap, pos, size, style):
        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style)
        self.bgcolor = wx.Brush(wx.WHITE)

    def SetBackgroundColour(self, color):
        self.bgcolor = wx.Brush(color)

    def GetBackgroundBrush(self, dc):
        return self.bgcolor