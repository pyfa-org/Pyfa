# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit


class AddBrowsedFits(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext not in ('projected', 'commandView', 'graphFitList', 'graphTgtList'):
            return False
        return True

    def getText(self, callingWindow, itmContext):
        return 'Add Fit...'

    def activate(self, callingWindow, fullContext, i):
        dlg = FitBrowserLiteDialog(self.mainFrame)
        if dlg.ShowModal() == wx.ID_OK:
            pass


AddBrowsedFits.register()


class FitBrowserLiteDialog(wx.Dialog):

    def __init__(self, parent):
        from gui.builtinViews.fitListLite import FitListView
        wx.Dialog.__init__(self, parent, title='Add Fits', style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((400, 400))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        searchBox = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        searchSizer.Add(searchBox, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(searchSizer, 0, wx.EXPAND | wx.ALL, 0)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromList = FitListView(self)
        listSizer.Add(fromList, 1, wx.EXPAND | wx.ALL, 5)

        listButtonSizer = wx.BoxSizer(wx.VERTICAL)
        listButtonSizer.AddStretchSpacer()
        addButton = wx.Button(self, wx.ID_ANY, '>>', wx.DefaultPosition, wx.DefaultSize, 0)
        listButtonSizer.Add(addButton, 0, wx.EXPAND | wx.ALL, 5)
        removeButton = wx.Button(self, wx.ID_ANY, '<<', wx.DefaultPosition, wx.DefaultSize, 0)
        listButtonSizer.Add(removeButton, 0, wx.EXPAND | wx.ALL, 5)
        listButtonSizer.AddStretchSpacer()
        listSizer.Add(listButtonSizer, 0, wx.EXPAND | wx.ALL, 5)

        toList = FitListView(self)
        listSizer.Add(toList, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(listSizer, 1, wx.EXPAND | wx.ALL, 0)

        buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if buttonSizer:
            mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALL, 5)

        fits = Fit.getInstance().getAllFitsLite()
        fromList.updateData(fits)

        self.SetSizer(mainSizer)
        self.CenterOnParent()
        self.Fit()
        searchBox.SetFocus()
