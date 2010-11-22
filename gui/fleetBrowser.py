import wx
import copy
from gui import bitmapLoader
import gui.mainFrame
from gui.PFListPane import PFListPane

FleetSelected, EVT_FLEET_SELECTED = wx.lib.newevent.NewEvent()


class FleetBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.fleetItemContainer = PFFleetItemContainer(self)
        for i in xrange(10):
            self.fleetItemContainer.AddWidget(FleetItem(self, 1, "IMBA Fleet #%d" % i, i, size = (0,32)))

        mainSizer.Add(self.fleetItemContainer, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
        self.Layout()
        self.fleetItemContainer.Layout()
        self.fleetItemContainer.RefreshList(True)
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

    def SelectWidget(self, widgetWnd):
        wlist = self.GetWidgetList()
        if self.selectedWidget != -1:
            wlist[self.selectedWidget].SetSelected(False)
            wlist[self.selectedWidget].Refresh()
        windex = self.GetWidgetIndex(widgetWnd)
        wlist[windex].SetSelected(True)
        wlist[windex].Refresh()
        self.selectedWidget = windex

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
                 size=(0,16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
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
        self.Parent.SelectWidget(self)
        self.Refresh()
        wx.PostEvent(self.mainFrame, FleetSelected(fleetID=0))
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


