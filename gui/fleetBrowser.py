import wx
from wx.lib.buttons import GenBitmapButton

import service.fleet
import gui.mainFrame
import gui.utils.colorUtils as colorUtils
import gui.sfBrowserItem as SFItem
from gui.bitmapLoader import BitmapLoader
from gui.PFListPane import PFListPane
from gui.utils.drawUtils import GetPartialText


FleetSelected, EVT_FLEET_SELECTED = wx.lib.newevent.NewEvent()
FleetRenamed, EVT_FLEET_RENAMED = wx.lib.newevent.NewEvent()
FleetRemoved, EVT_FLEET_REMOVED = wx.lib.newevent.NewEvent()
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

        self.m_sl2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_sl2, 0, wx.EXPAND, 0)

        self.fleetItemContainer = PFFleetItemContainer(self)

        mainSizer.Add(self.fleetItemContainer, 1, wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Layout()

        self.filter = ""
        self.fleetIDMustEditName = -1

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

        self.fleetIDMustEditName = newFleet.ID
        self.AddItem(newFleet.ID, newFleet.name, newFleet.count())

    def SelectFleetItem(self, event):
        fleetID = event.fleetID
        self.fleetItemContainer.SelectWidgetByFleetID(fleetID)
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=fleetID))

    def CopyFleetItem(self, event):
        fleetID = event.fleetID
        fleet = self.sFleet.copyFleetByID(fleetID)

        fleetName = fleet.name + " Copy"
        self.sFleet.renameFleet(fleet, fleetName)

        self.fleetIDMustEditName = fleet.ID
        self.AddItem(fleet.ID, fleet.name, fleet.count())

        self.fleetItemContainer.SelectWidgetByFleetID(fleet.ID)
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=fleet.ID))

    def RenameFleetItem(self, event):
        fleetID = event.fleetID
        fleet = self.sFleet.getFleetByID(fleetID)

        newFleetName = event.fleetName

        self.sFleet.renameFleet(fleet, newFleetName)
        wx.PostEvent(self.mainFrame, FleetRenamed(fleetID=fleet.ID))

    def DeleteFleetItem(self, event):
        self.sFleet.deleteFleetByID(event.fleetID)
        self.PopulateFleetList()
        wx.PostEvent(self.mainFrame, FleetRemoved(fleetID=event.fleetID))

    def AddItem(self, ID, name, count):
        self.fleetItemContainer.AddWidget(FleetItem(self, ID, name, count))
        widget = self.fleetItemContainer.GetWidgetByFleetID(ID)
        self.fleetItemContainer.RefreshList(True)
        self.fleetItemContainer.ScrollChildIntoView(widget)
        wx.PostEvent(self, FleetItemSelect(fleetID=ID))

    def PopulateFleetList(self):
        self.Freeze()
        filter_ = self.filter
        self.fleetItemContainer.RemoveAllChildren()
        fleetList = self.sFleet.getFleetList()
        for fleetID, fleetName, fleetCount in fleetList:
            if fleetName.lower().find(filter_.lower()) != -1:
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


class FleetBrowserHeader(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 24), style=wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.newBmp = BitmapLoader.getBitmap("fit_add_small", "gui")
        bmpSize = (16, 16)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        if 'wxMac' in wx.PlatformInfo:
            bgcolour = wx.Colour(0, 0, 0, 0)
        else:
            bgcolour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)

        self.fbNewFleet = PFGenBitmapButton(self, wx.ID_ANY, self.newBmp, wx.DefaultPosition, bmpSize, wx.BORDER_NONE)
        mainSizer.Add(self.fbNewFleet, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, 5)
        self.fbNewFleet.SetBackgroundColour(bgcolour)

        self.sl1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        mainSizer.Add(self.sl1, 0, wx.EXPAND | wx.LEFT, 5)

        self.tcFilter = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.tcFilter, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.stStatus = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stStatus.Wrap(-1)
        mainSizer.Add(self.stStatus, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

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
        wx.PostEvent(self.Parent, FleetItemNew(fleetName="New Fleet"))

    def fbNewEnterWindow(self, event):
        self.stStatus.SetLabel("New fleet")
        self.Parent.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        event.Skip()

    def fbHItemLeaveWindow(self, event):
        self.stStatus.SetLabel("")
        self.Parent.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def fbFilterEnterWindow(self, event):
        self.stStatus.SetLabel("Filter list")
        event.Skip()


class PFFleetItemContainer(PFListPane):
    def __init__(self, parent):
        PFListPane.__init__(self, parent)
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


class FleetItem(SFItem.SFBrowserItem):
    def __init__(self, parent, fleetID, fleetName, fleetCount,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0, 40), style=0):
        SFItem.SFBrowserItem.__init__(self, parent, size=size)

        self.fleetBrowser = self.Parent
        self.fleetID = fleetID
        self.fleetName = fleetName
        self.fleetCount = fleetCount

        self.padding = 4

        self.fontBig = wx.FontFromPixelSize((0, 15), wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.fontNormal = wx.FontFromPixelSize((0, 14), wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.fontSmall = wx.FontFromPixelSize((0, 12), wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.copyBmp = BitmapLoader.getBitmap("fit_add_small", "gui")
        self.renameBmp = BitmapLoader.getBitmap("fit_rename_small", "gui")
        self.deleteBmp = BitmapLoader.getBitmap("fit_delete_small", "gui")
        self.acceptBmp = BitmapLoader.getBitmap("faccept_small", "gui")
        self.fleetBmp = BitmapLoader.getBitmap("fleet_item_big", "gui")

        fleetImg = self.fleetBmp.ConvertToImage()
        fleetImg = fleetImg.Blur(2)

        if not fleetImg.HasAlpha():
            fleetImg.InitAlpha()

        fleetImg = fleetImg.AdjustChannels(1, 1, 1, 0.5)
        self.fleetEffBmp = wx.BitmapFromImage(fleetImg)

        self.toolbar.AddButton(self.copyBmp, "Copy", self.CopyFleetCB)
        self.renameBtn = self.toolbar.AddButton(self.renameBmp, "Rename", self.RenameFleetCB)
        self.toolbar.AddButton(self.deleteBmp, "Delete", self.DeleteFleetCB)

        self.editWidth = 150
        self.tcFleetName = wx.TextCtrl(self, wx.ID_ANY, "%s" % self.fleetName, wx.DefaultPosition, (self.editWidth, -1), wx.TE_PROCESS_ENTER)

        if self.fleetBrowser.fleetIDMustEditName != self.fleetID:
            self.tcFleetName.Show(False)
        else:
            self.tcFleetName.SetFocus()
            self.tcFleetName.SelectAll()
            self.fleetBrowser.fleetIDMustEditName = -1
            self.renameBtn.SetBitmap(self.acceptBmp)
            self.selected = True

        self.tcFleetName.Bind(wx.EVT_KILL_FOCUS, self.OnEditLostFocus)
        self.tcFleetName.Bind(wx.EVT_TEXT_ENTER, self.RenameFleet)
        self.tcFleetName.Bind(wx.EVT_KEY_DOWN, self.EditCheckEsc)

        self.animCount = 0

    def MouseLeftUp(self, event):
        if self.tcFleetName.IsShown():
            self.RestoreEditButton()
        else:
            wx.PostEvent(self.fleetBrowser, FleetItemSelect(fleetID=self.fleetID))

    def CopyFleetCB(self):
        if self.tcFleetName.IsShown():
            self.RestoreEditButton()
            return

        wx.PostEvent(self.fleetBrowser, FleetItemCopy(fleetID=self.fleetID))

    def RenameFleetCB(self):

        if self.tcFleetName.IsShown():

            self.RenameFleet(None)
            self.RestoreEditButton()

        else:
            self.tcFleetName.SetValue(self.fleetName)
            self.tcFleetName.Show()

            self.renameBtn.SetBitmap(self.acceptBmp)
            self.Refresh()

            self.tcFleetName.SetFocus()
            self.tcFleetName.SelectAll()

            self.Refresh()

    def RenameFleet(self, event):

        newFleetName = self.tcFleetName.GetValue()
        self.fleetName = newFleetName

        self.tcFleetName.Show(False)

        wx.PostEvent(self.fleetBrowser, FleetItemRename(fleetID=self.fleetID, fleetName=self.fleetName))
        self.Refresh()

    def DeleteFleetCB(self):
        if self.tcFleetName.IsShown():
            self.RestoreEditButton()
            return
        wx.PostEvent(self.fleetBrowser, FleetItemDelete(fleetID=self.fleetID))

    def RestoreEditButton(self):
            self.tcFleetName.Show(False)
            self.renameBtn.SetBitmap(self.renameBmp)
            self.Refresh()

    def OnEditLostFocus(self, event):
        self.RestoreEditButton()
        self.Refresh()

    def EditCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.RestoreEditButton()
        else:
            event.Skip()

    def IsSelected(self):
        return self.selected

    def UpdateElementsPos(self, mdc):
        rect = self.GetRect()

        self.toolbarx = rect.width - self.toolbar.GetWidth() - self.padding
        self.toolbary = (rect.height - self.toolbar.GetHeight()) / 2

        self.toolbarx = self.toolbarx + self.animCount

        self.fleetBmpx = self.padding + (rect.height - self.fleetBmp.GetWidth()) / 2
        self.fleetBmpy = (rect.height - self.fleetBmp.GetHeight()) / 2

        self.fleetBmpx -= self.animCount

        self.textStartx = self.fleetBmpx + self.fleetBmp.GetWidth() + self.padding

        self.fleetNamey = (rect.height - self.fleetBmp.GetHeight()) / 2

        mdc.SetFont(self.fontBig)
        wtext, htext = mdc.GetTextExtent(self.fleetName)

        self.fleetCounty = self.fleetNamey + htext

        mdc.SetFont(self.fontSmall)

        wlabel, hlabel = mdc.GetTextExtent(self.toolbar.hoverLabel)

        self.thoverx = self.toolbarx - self.padding - wlabel
        self.thovery = (rect.height - hlabel) / 2
        self.thoverw = wlabel

    def DrawItem(self, mdc):
        # rect = self.GetRect()

        windowColor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        textColor = colorUtils.GetSuitableColor(windowColor, 1)

        mdc.SetTextForeground(textColor)

        self.UpdateElementsPos(mdc)

        self.toolbar.SetPosition((self.toolbarx, self.toolbary))
        mdc.DrawBitmap(self.fleetEffBmp, self.fleetBmpx + 3, self.fleetBmpy + 2)
        mdc.DrawBitmap(self.fleetBmp, self.fleetBmpx, self.fleetBmpy)

        mdc.SetFont(self.fontNormal)

        suffix = "%d ships" % self.fleetCount if self.fleetCount > 1 else "%d ship" % self.fleetCount if self.fleetCount == 1 else "No ships"
        fleetCount = "Fleet size: %s" % suffix
        fleetCount = GetPartialText(mdc, fleetCount, self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)

        mdc.DrawText(fleetCount, self.textStartx, self.fleetCounty)

        mdc.SetFont(self.fontSmall)
        mdc.DrawText(self.toolbar.hoverLabel, self.thoverx, self.thovery)

        mdc.SetFont(self.fontBig)

        pfname = GetPartialText(mdc, self.fleetName, self.toolbarx - self.textStartx - self.padding * 2 - self.thoverw)
        mdc.DrawText(pfname, self.textStartx, self.fleetNamey)

        if self.tcFleetName.IsShown():
            self.AdjustControlSizePos(self.tcFleetName, self.textStartx, self.toolbarx - self.editWidth - self.padding)

    def AdjustControlSizePos(self, editCtl, start, end):
        fnEditSize = editCtl.GetSize()
        wSize = self.GetSize()
        fnEditPosX = end
        fnEditPosY = (wSize.height - fnEditSize.height) / 2
        if fnEditPosX < start:
            editCtl.SetSize((self.editWidth + fnEditPosX - start, -1))
            editCtl.SetPosition((start, fnEditPosY))
        else:
            editCtl.SetSize((self.editWidth, -1))
            editCtl.SetPosition((fnEditPosX, fnEditPosY))


class PFGenBitmapButton(GenBitmapButton):
    def __init__(self, parent, id, bitmap, pos, size, style):
        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style)
        self.bgcolor = wx.Brush(wx.WHITE)

    def SetBackgroundColour(self, color):
        self.bgcolor = wx.Brush(color)

    def GetBackgroundBrush(self, dc):
        return self.bgcolor
