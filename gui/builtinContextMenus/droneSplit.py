import re

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class DroneSplit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('droneSplit'):
            return False

        return srcContext == "droneItem" and selection[0].amount > 1

    def getText(self, itmContext, selection):
        return "Split {0} Stack".format(itmContext)

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        drone = selection[0]
        dlg = DroneStackSplit(self.mainFrame, drone.amount)

        if dlg.ShowModal() == wx.ID_OK:

            if dlg.input.GetLineText(0).strip() == '':
                return

            fitID = self.mainFrame.getActiveFit()
            fit = Fit.getInstance().getFit(fitID)
            cleanInput = re.sub(r'[^0-9.]', '', dlg.input.GetLineText(0).strip())

            self.mainFrame.command.Submit(cmd.GuiSplitLocalDroneStackCommand(
                fitID=fitID,
                position=fit.drones.index(drone),
                amount=int(cleanInput)))


DroneSplit.register()


class DroneStackSplit(wx.Dialog):

    def __init__(self, parent, value):
        wx.Dialog.__init__(self, parent, title="Split Drone Stack")
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
