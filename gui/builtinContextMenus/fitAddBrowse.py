import re

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
        titles = {
            'projected': 'Add Projected Fits',
            'commandView': 'Add Command Fits',
            'graphFitList': 'Add Fits to Graph',
            'graphTgtList': 'Add Targets to Graph'}
        dlg = FitBrowserLiteDialog(self.mainFrame, title=titles[fullContext[0]])
        if dlg.ShowModal() == wx.ID_OK:
            pass


AddBrowsedFits.register()


class FitBrowserLiteDialog(wx.Dialog):

    def __init__(self, parent, title='Add Fits'):
        wx.Dialog.__init__(self, parent, title=title, style=wx.DEFAULT_DIALOG_STYLE)

        from gui.builtinViews.fitListLite import FitListView

        self.sFit = Fit.getInstance()
        self.allFits = sorted(self.sFit.getAllFitsLite(), key=lambda f: (f.shipName, f.name))
        self.SetMinSize((400, 400))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.searchBox = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        searchSizer.Add(self.searchBox, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(searchSizer, 0, wx.EXPAND | wx.ALL, 0)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fromList = FitListView(self)
        listSizer.Add(self.fromList, 1, wx.EXPAND | wx.ALL, 5)

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

        self.resetContents()

        self.inputTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnInputTimer, self.inputTimer)
        self.searchBox.Bind(event=wx.EVT_TEXT, handler=self.OnSearchChanged)

        self.SetSizer(mainSizer)
        self.Layout()
        self.SetSize(self.GetBestSize())
        self.CenterOnParent()
        self.searchBox.SetFocus()

    def OnSearchChanged(self, event):
        event.Skip()
        self.inputTimer.Stop()
        self.inputTimer.Start(self.sFit.serviceFittingOptions['marketSearchDelay'], True)

    def OnInputTimer(self, event):
        event.Skip()
        searchPattern = self.searchBox.GetValue().strip()
        if not searchPattern:
            self.resetContents()
        else:

            def isMatch(fit, searchTokens):
                for token in searchTokens:
                    if token not in fit.name.lower() and token not in fit.shipName.lower():
                        return False
                return True

            matches = []
            searchTokens = [t.lower() for t in re.split('\s+', searchPattern)]
            for fit in self.allFits:
                if isMatch(fit, searchTokens):
                    matches.append(fit)
            self.fromList.updateData(matches)

    def resetContents(self):
        self.fromList.updateData(self.allFits)
