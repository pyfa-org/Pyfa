import wx
from wx.lib.buttons import GenBitmapButton


class PFGenBitmapButton(GenBitmapButton):
    def __init__(self, parent, id, bitmap, pos, size, style):
        GenBitmapButton.__init__(self, parent, id, bitmap, pos, size, style)
        self.bgcolor = wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColorChanged)

    def SetBackgroundColour(self, color):
        self.bgcolor = wx.Brush(color)

    def GetBackgroundBrush(self, dc):
        return self.bgcolor

    def OnSysColorChanged(self, event):
        self.bgcolor = wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.Refresh()
        event.Skip()
