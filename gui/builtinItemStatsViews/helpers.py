# noinspection PyPackageRequirements
import wx

# noinspection PyPackageRequirements
import wx.lib.mixins.listctrl as listmix

from gui.utils.dark import isDark


class AutoListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)
        self.ApplyThemeColors()
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColorChanged)

    def ApplyThemeColors(self):
        self._defaultb = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        # None lets the mixin fall back to the system alternating color
        highlight = self._defaultb.ChangeLightness(110) if isDark() else None
        listmix.ListRowHighlighter.SetHighlightColor(self, highlight)

    def OnSysColorChanged(self, event):
        self.ApplyThemeColors()
        self.RefreshRows()
        event.Skip()

class AutoListCtrlNoHighlight(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
