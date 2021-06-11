# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.utils.helpers_wxPython import HandleCtrlBackspace
from gui.utils.numberFormatter import formatAmount
from service.fit import Fit


class NotesView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lastFitId = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.editNotes = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.BORDER_NONE)
        mainSizer.Add(self.editNotes, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainSizer)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_TEXT, self.onText)
        self.editNotes.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.changeTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.delayedSave, self.changeTimer)

    def OnKeyDown(self, event):
        if event.RawControlDown() and event.GetKeyCode() == wx.WXK_BACK:
            try:
                HandleCtrlBackspace(self.editNotes)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pass
        else:
            event.Skip()

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        self.changeTimer.Stop()  # cancel any pending timers

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # when switching fits, ensure that we save the notes for the previous fit
        if self.lastFitId is not None:
            sFit.editNotes(self.lastFitId, self.editNotes.GetValue())

        if activeFitID is None and self.lastFitId is not None:
            self.lastFitId = None
            return
        elif activeFitID != self.lastFitId:
            self.lastFitId = activeFitID
            self.editNotes.ChangeValue(fit.notes or "")
            wx.PostEvent(self.mainFrame, GE.FitNotesChanged())

    def onText(self, event):
        # delay the save so we're not writing to sqlite on every keystroke
        self.changeTimer.Stop()  # cancel the existing timer
        self.changeTimer.Start(1000, True)

    def delayedSave(self, event):
        event.Skip()
        sFit = Fit.getInstance()
        sFit.editNotes(self.lastFitId, self.editNotes.GetValue())
        wx.PostEvent(self.mainFrame, GE.FitNotesChanged())

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active implants
        if opt in (1, 2):
            amount = len(self.editNotes.GetValue())
            return ' ({})'.format(formatAmount(amount, 2, 0, 3)) if amount else None
        else:
            return None
