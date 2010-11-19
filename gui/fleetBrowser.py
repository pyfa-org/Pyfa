import wx
import copy

FleetSelected, EVT_FLEET_SELECTED = wx.lib.newevent.NewEvent()

class FleetItem(wx.Window):
    def __init__(self, parent, fleetID, fleetName, fleetCount,
                 id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(0,16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.fleetID = fleetID
        self.fleetName = fleetName
        self.fleetCount = fleetCount
        self.highlighted = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Bind(wx.EVT_LEAVE_WINDOW, self.LeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.EnterWindow)

    def Rename(self, newName):
        self.fleetName = newName

    def Delete(self):
        print "Delete stuff..."

    def Copy(self):
        print "Copy"

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
            bdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            bdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
            bdc.Clear()

    def EnterWindow(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def LeaveWindow(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()



class FleetBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("pink")
        x = FleetItem(self, 1, 1, 1, size = (200,32))