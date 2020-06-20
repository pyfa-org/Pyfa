import re

# noinspection PyPackageRequirements
import wx

import gui.display as d
from service.fit import Fit

_t = wx.GetTranslation

def fitSorter(fit):
    return fit.shipName, fit.name


class FitBrowserLiteDialog(wx.Dialog):

    def __init__(self, parent, title=_t('Add Fits'), excludedFitIDs=()):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE)

        listWidth = 250 if 'wxGTK' in wx.PlatformInfo else 200

        self.sFit = Fit.getInstance()
        self.allFits = sorted(
            (f for f in self.sFit.getAllFitsLite() if f.ID not in excludedFitIDs),
            key=fitSorter)
        self.SetMinSize((400, 400))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.searchBox = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        searchSizer.Add(self.searchBox, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(searchSizer, 0, wx.EXPAND | wx.ALL, 0)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fromList = FitListView(self, size=(listWidth, -1))
        self.fromList.Bind(wx.EVT_LEFT_DCLICK, self.OnFromListDclick)
        listSizer.Add(self.fromList, 1, wx.EXPAND | wx.ALL, 5)

        listButtonSizer = wx.BoxSizer(wx.VERTICAL)
        listButtonSizer.AddStretchSpacer()
        addButton = wx.Button(self, wx.ID_ANY, '>>', wx.DefaultPosition, wx.DefaultSize, 0)
        addButton.Bind(wx.EVT_BUTTON, self.OnButtonAdd)
        listButtonSizer.Add(addButton, 0, wx.EXPAND | wx.ALL, 5)
        removeButton = wx.Button(self, wx.ID_ANY, '<<', wx.DefaultPosition, wx.DefaultSize, 0)
        removeButton.Bind(wx.EVT_BUTTON, self.OnButtonRemove)
        listButtonSizer.Add(removeButton, 0, wx.EXPAND | wx.ALL, 5)
        listButtonSizer.AddStretchSpacer()
        listSizer.Add(listButtonSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.toList = FitListView(self, size=(listWidth, -1))
        self.toList.Bind(wx.EVT_LEFT_DCLICK, self.OnToListDclick)
        listSizer.Add(self.toList, 1, wx.EXPAND | wx.ALL, 5)
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

    def OnButtonAdd(self, event):
        event.Skip()
        fits = self.fromList.GetSelectedFits()
        if not fits:
            return
        self.fromList.removeFits(fits)
        self.toList.addFits(fits)
        self.fromList.unselectAll()
        self.toList.unselectAll()

    def OnButtonRemove(self, event):
        event.Skip()
        fits = self.toList.GetSelectedFits()
        if not fits:
            return
        self.toList.removeFits(fits)
        self.fromList.addFits(fits)
        self.fromList.unselectAll()
        self.toList.unselectAll()

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
                    if (
                        token not in fit.name.lower() and
                        token not in fit.shipName.lower() and
                        token not in fit.shipNameShort.lower()
                    ):
                        return False
                return True

            matches = []
            searchTokens = [t.lower() for t in re.split('\s+', searchPattern)]
            for fit in self.allFits:
                if isMatch(fit, searchTokens):
                    matches.append(fit)
            self.fromList.updateData(matches)

    def OnFromListDclick(self, event):
        event.Skip()
        row, _ = self.fromList.HitTest(event.Position)
        if row == -1:
            return
        try:
            fit = self.fromList.fits[row]
        except IndexError:
            return
        self.fromList.removeFits([fit])
        self.toList.addFits([fit])
        self.fromList.unselectAll()
        self.toList.unselectAll()

    def OnToListDclick(self, event):
        event.Skip()
        row, _ = self.toList.HitTest(event.Position)
        if row == -1:
            return
        try:
            fit = self.toList.fits[row]
        except IndexError:
            return
        self.toList.removeFits([fit])
        self.fromList.addFits([fit])
        self.fromList.unselectAll()
        self.toList.unselectAll()

    def resetContents(self):
        fits = [f for f in self.allFits if f not in self.toList.fits]
        self.fromList.updateData(fits)

    def getFitIDsToAdd(self):
        return [f.ID for f in self.toList.fits]


class FitListView(d.Display):

    DEFAULT_COLS = ['Base Name']

    def __init__(self, parent, **kwargs):
        super().__init__(parent, style=wx.BORDER_NONE, **kwargs)
        self.fits = []

    def updateView(self):
        self.update(self.fits)

    def refreshView(self):
        self.refresh(self.fits)

    def updateData(self, fits):
        self.fits = fits
        self.updateView()

    def addFits(self, fits):
        for fit in fits:
            if fit in self.fits:
                continue
            self.fits.append(fit)
        self.fits.sort(key=fitSorter)
        self.updateView()

    def removeFits(self, fits):
        for fit in fits:
            if fit not in self.fits:
                continue
            self.fits.remove(fit)
        self.updateView()

    def GetSelectedFits(self):
        fits = []
        for row in self.getSelectedRows():
            try:
                fit = self.fits[row]
            except IndexError:
                continue
            fits.append(fit)
        return fits
