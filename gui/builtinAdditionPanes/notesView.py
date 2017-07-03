# noinspection PyPackageRequirements
import wx

from service.fit import Fit
import gui.globalEvents as GE
import gui.mainFrame


class NotesView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lastFitId = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.editNotes = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.BORDER_NONE, )
        mainSizer.Add(self.editNotes, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_TEXT, self.onText)
        self.saveTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.delayedSave, self.saveTimer)

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        self.saveTimer.Stop()  # cancel any pending timers

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # when switching fits, ensure that we save the notes for the previous fit
        if self.lastFitId is not None:
            sFit.editNotes(self.lastFitId, self.editNotes.GetValue())

        if event.fitID is None and self.lastFitId is not None:
            self.lastFitId = None
            event.Skip()
            return
        elif event.fitID != self.lastFitId:
            self.lastFitId = event.fitID
            self.editNotes.SetValue(fit.notes or "")

        event.Skip()

    def onText(self, event):
        # delay the save so we're not writing to sqlite on every keystroke
        self.saveTimer.Stop()  # cancel the existing timer
        self.saveTimer.Start(1000, True)

    def delayedSave(self, event):
        sFit = Fit.getInstance()
        sFit.editNotes(self.lastFitId, self.editNotes.GetValue())
