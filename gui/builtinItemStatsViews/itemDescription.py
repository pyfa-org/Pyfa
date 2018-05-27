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

        bgcolor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        fgcolor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

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

        self.description.Bind(wx.EVT_CONTEXT_MENU, self.onPopupMenu)
        self.description.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

        self.popupMenu = wx.Menu()
        copyItem = wx.MenuItem(self.popupMenu, 1, 'Copy')
        self.popupMenu.Append(copyItem)
        self.popupMenu.Bind(wx.EVT_MENU, self.menuClickHandler, copyItem)

    def onPopupMenu(self, event):
        self.PopupMenu(self.popupMenu)

    def menuClickHandler(self, event):
        selectedMenuItem = event.GetId()
        if selectedMenuItem == 1:  # Copy was chosen
            self.copySelectionToClipboard()

    def onKeyDown(self, event):
        keyCode = event.GetKeyCode()
        # Ctrl + C
        if keyCode == 67 and event.ControlDown():
            self.copySelectionToClipboard()
        # Ctrl + A
        if keyCode == 65 and event.ControlDown():
            self.description.SelectAll()

    def copySelectionToClipboard(self):
        selectedText = self.description.SelectionToText()
        if selectedText == '':  # if no selection, copy all content
            selectedText = self.description.ToText()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(selectedText))
            wx.TheClipboard.Close()
