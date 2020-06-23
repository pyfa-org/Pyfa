import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class ImplantSetSave(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext not in ('implantItemMisc', 'implantItemMiscChar'):
            return False

        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        self.implants = fit.appliedImplants[:]
        if not self.implants:
            return False

        return True

    def getText(self, callingWindow, context):
        return _t('Save as New Implant Set')

    def activate(self, callingWindow, fullContext, i):
        with NameDialog(self.mainFrame, '') as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.input.GetLineText(0).strip()
                if name == '':
                    return
                from gui.setEditor import ImplantSetEditor
                ImplantSetEditor.openOne(parent=self.mainFrame, dataToAdd=(name, self.implants))


ImplantSetSave.register()


class NameDialog(wx.Dialog):

    def __init__(self, parent, value):
        super().__init__(parent, title=_t('New Implant Set'), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, _t('Enter a name for your new Implant Set:'))
        bSizer2.Add(text, 0)

        bSizer1.Add(bSizer2, 0, wx.ALL, 10)

        self.input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        if value is None:
            value = ''
        else:
            value = str(value)
        self.input.SetValue(value)
        self.input.SelectAll()

        bSizer1.Add(self.input, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 15)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 15)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.input.SetFocus()
        self.input.Bind(wx.EVT_TEXT_ENTER, self.processEnter)
        self.SetSizer(bSizer1)
        self.CenterOnParent()
        self.Fit()

    def processEnter(self, evt):
        self.EndModal(wx.ID_OK)
