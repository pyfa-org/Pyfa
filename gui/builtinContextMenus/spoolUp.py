import gui.mainFrame
from gui.contextMenu import ContextMenu
# noinspection PyPackageRequirements
from service.settings import ContextMenuSettings
import wx
from eos.utils.spoolSupport import SpoolType
import gui.fitCommands as cmd


class SpoolUp(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('project'):
            return False

        if srcContext not in ("fittingModule") or self.mainFrame.getActiveFit() is None:
            return False

        item = selection[0]

        return item.item.group.name in ('Precursor Weapon')

    def getText(self, itmContext, selection):
        return "Set Spoolup".format(itmContext)

    def activate(self, fullContext, selection, i):
        thing = selection[0]
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        fitID = mainFrame.getActiveFit()
        srcContext = fullContext[0]

        while True:
            dlg = SpoolUpChanger(self.mainFrame, thing)
            if dlg.ShowModal() != wx.ID_OK:
                break

            type = dlg.spoolChoice.GetClientData(dlg.spoolChoice.GetSelection())
            amount = dlg.input.GetValue()

            if type == SpoolType.SCALE:
                if amount < 0 or amount > 100:
                    dlg = wx.MessageDialog(self.mainFrame, "The amount provided  isn't within the range of 0 - 100.", "Error", wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    continue
                amount = amount / 100
            if type is None:
                amount = None

            self.mainFrame.command.Submit(cmd.GuiSetSpoolup(fitID, thing, type, amount))
            return


SpoolUp.register()


class SpoolUpChanger(wx.Dialog):

    spoolTypes = {
        None: ("Default", "pyfa defaults to using 'scale' calculation with 100%"),
        SpoolType.SCALE: ("Scale", "Amount is a percentage from 0 - 100; rounds down to closest module cycle."),
        SpoolType.TIME: ("Time (s)", "Amount defines time in seconds since spoolup module was activated."),
        SpoolType.CYCLES: ("Cycles", "Amount is number of cycles module went through since being activated.")
    }

    def __init__(self, parent, module):
        wx.Dialog.__init__(self, parent, title="Change Spool-Up")
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, wx.ID_ANY, "Type:")
        bSizer2.Add(text, 0)

        self.spoolChoice = wx.Choice(self, wx.ID_ANY, style=0)

        for k, v in self.spoolTypes.items():
            i = self.spoolChoice.Append(v[0], k)
            if module.spoolType == k:
                self.spoolChoice.SetSelection(i)

        self.spoolChoice.Bind(wx.EVT_CHOICE, self.spoolTypeChanged)


        bSizer2.Add(self.spoolChoice, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 5)

        self.spoolDesc = wx.StaticText(self, wx.ID_ANY, self.spoolTypes[module.spoolType][1])
        bSizer2.Add(self.spoolDesc, 1)

        text1 = wx.StaticText(self, wx.ID_ANY, "Amount:")
        bSizer2.Add(text1, 0, wx.TOP, 10)

        bSizer1.Add(bSizer2, 0, wx.ALL, 10)

        self.input = wx.SpinCtrlDouble(self, min=0, max=1000)

        bSizer1.Add(self.input, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 15)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.input.SetValue(module.spoolAmount or 0)
        self.input.SetFocus()
        self.input.Bind(wx.EVT_TEXT_ENTER, self.processEnter)
        self.SetSizer(bSizer1)
        self.CenterOnParent()
        self.Fit()

    def spoolTypeChanged(self, evt):
        self.input.Enable(evt.ClientData is not None)
        self.spoolDesc.SetLabel(self.spoolTypes[evt.ClientData][1])
        self.Layout()

    def processEnter(self, evt):
        self.EndModal(wx.ID_OK)
