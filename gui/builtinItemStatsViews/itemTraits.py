# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import wx.html


class ItemTraits(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.traits = wx.html.HtmlWindow(self)
        self.traits.SetPage(item.traits.traitText)

        mainSizer.Add(self.traits, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()
