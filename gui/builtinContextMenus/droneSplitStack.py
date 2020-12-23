import re

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class DroneSplitStack(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != "droneItem":
            return False

        if mainItem is None:
            return False

        return mainItem.amount > 1

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Split {} Stack").format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        with DroneStackSplit(self.mainFrame, mainItem.amount) as dlg:

            if dlg.ShowModal() == wx.ID_OK:

                if dlg.input.GetLineText(0).strip() == '':
                    return

                fitID = self.mainFrame.getActiveFit()
                fit = Fit.getInstance().getFit(fitID)
                cleanInput = re.sub(r'[^0-9.]', '', dlg.input.GetLineText(0).strip())

                if mainItem in fit.drones:
                    position = fit.drones.index(mainItem)
                    self.mainFrame.command.Submit(cmd.GuiSplitLocalDroneStackCommand(
                            fitID=fitID, position=position, amount=int(cleanInput)))


DroneSplitStack.register()


class DroneStackSplit(wx.Dialog):

    def __init__(self, parent, value):
        super().__init__(parent, title="Split Drone Stack", style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, "New Amount:")
        bSizer2.Add(text, 0)

        bSizer1.Add(bSizer2, 0, wx.ALL, 10)

        self.input = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.input.SetValue(str(value))
        self.input.SelectAll()

        bSizer1.Add(self.input, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 15)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        bSizer3.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.BOTTOM | wx.EXPAND, 15)

        bSizer3.Add(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND)
        bSizer1.Add(bSizer3, 0, wx.ALL | wx.EXPAND, 10)

        self.input.SetFocus()
        self.input.Bind(wx.EVT_CHAR, self.onChar)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.processEnter)
        self.SetSizer(bSizer1)
        self.CenterOnParent()
        self.Fit()

    def processEnter(self, evt):
        self.EndModal(wx.ID_OK)

    # checks to make sure it's valid number
    @staticmethod
    def onChar(event):
        key = event.GetKeyCode()

        acceptable_characters = "1234567890"
        acceptable_keycode = [3, 22, 13, 8, 127]  # modifiers like delete, copy, paste
        if key in acceptable_keycode or key >= 255 or (key < 255 and chr(key) in acceptable_characters):
            event.Skip()
            return
        else:
            return False
