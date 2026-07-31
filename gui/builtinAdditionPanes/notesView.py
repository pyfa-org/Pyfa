# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.utils.helpers_wxPython import HandleCtrlBackspace
from gui.utils.numberFormatter import formatAmount
from service.fit import Fit
from config import EVE_FIT_NOTE_MAX


LATER = 1000
'''timer interval, delay the save'''

# 3
EXPAND_LF_LEN = len("<br>") - 1
'''
If you save `Fit.notes` to "description" in eve fit(xml export),
newline characters must be converted to "<br>"
'''

def computeEVEFitDescSize(note):
    # type: (str) -> int
    return len(note) + (note.count("\n") * EXPAND_LF_LEN)

def ifExceedsTheUpperLimit(nv, note=None):
    # type: (wx.TextCtrl, str) -> None
    '''When the note size exceeds the upper limit, the text will turn red.'''
    if note is None: note = nv.GetValue()
    color = '#FF0000' if computeEVEFitDescSize(note) > EVE_FIT_NOTE_MAX else '#000000'
    nv.SetForegroundColour(color)
    nv.Refresh(False)


class NotesView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lastFitId = None
        self.changeTimer = wx.Timer(self)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.editNotes = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.BORDER_NONE)
        self.Bind(wx.EVT_TEXT, self.onText)
        self.Bind(wx.EVT_TIMER, self.delayedSave, self.changeTimer)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.editNotes.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.editNotes, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainSizer)

    def OnKeyDown(self, event):
        # type: (wx.KeyEvent) -> None
        nv = self.editNotes
        if event.RawControlDown() and event.GetKeyCode() == wx.WXK_BACK:
            try:
                HandleCtrlBackspace(nv)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pass
        else:
            event.Skip()

        ifExceedsTheUpperLimit(nv)

    def fitChanged(self, event):
        # type: (wx.Event) -> None
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
            note = fit.notes or ""
            nv = self.editNotes
            nv.ChangeValue(note)
            ifExceedsTheUpperLimit(nv, note)
            wx.PostEvent(self.mainFrame, GE.FitNotesChanged())

    def onText(self, event):
        # type: (wx.Event) -> None
        # delay the save so we're not writing to sqlite on every keystroke
        self.changeTimer.Stop()  # cancel the existing timer
        self.changeTimer.Start(LATER, True)
        # When the note size exceeds the upper limit, the text will turn red.
        ifExceedsTheUpperLimit(self.editNotes)

    def delayedSave(self, event):
        # type: (wx.Event) -> None
        event.Skip()
        sFit = Fit.getInstance()
        sFit.editNotes(self.lastFitId, self.editNotes.GetValue())
        wx.PostEvent(self.mainFrame, GE.FitNotesChanged())

    def getTabExtraText(self):
        # type: () -> str|None
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
            amount = computeEVEFitDescSize(self.editNotes.GetValue())
            return ' ({})'.format(formatAmount(amount, 2, 0, 3)) if amount else None
        else:
            return None
