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

        self.traits.Bind(wx.EVT_CONTEXT_MENU, self.showPopupMenu)

        mainSizer.Add(self.traits, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()

        self.popupMenu = wx.Menu()
        copyItem = wx.MenuItem(self.popupMenu, 1, 'Copy')
        self.popupMenu.Append(copyItem)
        self.popupMenu.Bind(wx.EVT_MENU, self.menuClickHandler, copyItem)

    def showPopupMenu(self, event):
        self.PopupMenu(self.popupMenu)

    def menuClickHandler(self, event):
        selectedMenuItem = event.GetId()
        if selectedMenuItem == 1:  # Copy was chosen
            selectedText = self.traits.SelectionToText()
            if len(selectedText) > 0:
                if wx.TheClipboard.Open():
                    wx.TheClipboard.SetData(wx.TextDataObject(selectedText))
                    wx.TheClipboard.Close()
