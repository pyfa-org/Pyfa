# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import wx.html
import re


class ItemDescription(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        bgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        fgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        self.description = wx.html.HtmlWindow(self)

        if not item.description:
            return

        desc = item.description.replace("\n", "<br>")
        # Strip font tags
        desc = re.sub("<( *)font( *)color( *)=(.*?)>(?P<inside>.*?)<( *)/( *)font( *)>", "\g<inside>", desc)
        # Strip URLs
        desc = re.sub("<( *)a(.*?)>(?P<inside>.*?)<( *)/( *)a( *)>", "\g<inside>", desc)
        desc = "<body bgcolor='" + bgcolor.GetAsString(wx.C2S_HTML_SYNTAX) + "' text='" + fgcolor.GetAsString(
                wx.C2S_HTML_SYNTAX) + "' >" + desc + "</body>"

        self.description.SetPage(desc)

        mainSizer.Add(self.description, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()
