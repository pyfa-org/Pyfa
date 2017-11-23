# noinspection PyPackageRequirements
import wx

# noinspection PyPackageRequirements
import wx.lib.mixins.listctrl as listmix


class AutoListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)


class AutoListCtrlNoHighlight(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
