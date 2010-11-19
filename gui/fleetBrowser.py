import wx

FleetSelected, EVT_FLEET_SELECTED = wx.lib.newevent.NewEvent()

class FleetBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("pink")
