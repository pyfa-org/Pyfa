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

        self.traits.Bind(wx.EVT_CONTEXT_MENU, self.onPopupMenu)
        self.traits.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

        mainSizer.Add(self.traits, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()

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
            self.traits.SelectAll()

    def copySelectionToClipboard(self):
        selectedText = self.traits.SelectionToText()
        if selectedText == '':  # if no selection, copy all content
            selectedText = self.traits.ToText()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(selectedText))
            wx.TheClipboard.Close()
