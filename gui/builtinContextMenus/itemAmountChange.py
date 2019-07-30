import re

# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.saveddata.cargo import Cargo as es_Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.fit import Fit as es_Fit
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit


class ChangeItemAmount(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("droneItem", "projectedDrone", "cargoItem", "projectedFit", "fighterItem", "projectedFighter"):
            return False

        if mainItem is None:
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return "Change {0} Quantity".format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        srcContext = fullContext[0]
        if isinstance(mainItem, es_Fit):
            try:
                value = mainItem.getProjectionInfo(fitID).amount
            except AttributeError:
                return
        elif isinstance(mainItem, es_Fighter):
            value = mainItem.amountActive
        else:
            value = mainItem.amount

        dlg = AmountChanger(self.mainFrame, value, (0, 20)) if isinstance(mainItem, es_Fit) else AmountChanger(self.mainFrame, value)
        if dlg.ShowModal() == wx.ID_OK:

            if dlg.input.GetLineText(0).strip() == '':
                return

            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            cleanInput = int(float(re.sub(r'[^0-9.]', '', dlg.input.GetLineText(0).strip())))

            if isinstance(mainItem, es_Cargo):
                self.mainFrame.command.Submit(cmd.GuiChangeCargoAmountCommand(
                    fitID=fitID, itemID=mainItem.itemID, amount=cleanInput))
            elif isinstance(mainItem, Drone):
                if srcContext == "projectedDrone":
                    self.mainFrame.command.Submit(cmd.GuiChangeProjectedDroneAmountCommand(
                        fitID=fitID, itemID=mainItem.itemID, amount=cleanInput))
                else:
                    if mainItem in fit.drones:
                        position = fit.drones.index(mainItem)
                        self.mainFrame.command.Submit(cmd.GuiChangeLocalDroneAmountCommand(
                            fitID=fitID, position=position, amount=cleanInput))
            elif isinstance(mainItem, es_Fit):
                self.mainFrame.command.Submit(cmd.GuiChangeProjectedFitAmountCommand(
                    fitID=fitID, projectedFitID=mainItem.ID, amount=cleanInput))
            elif isinstance(mainItem, es_Fighter):
                if srcContext == "projectedFighter":
                    if mainItem in fit.projectedFighters:
                        position = fit.projectedFighters.index(mainItem)
                        self.mainFrame.command.Submit(cmd.GuiChangeProjectedFighterAmountCommand(
                            fitID=fitID, position=position, amount=cleanInput))
                else:
                    if mainItem in fit.fighters:
                        position = fit.fighters.index(mainItem)
                        self.mainFrame.command.Submit(cmd.GuiChangeLocalFighterAmountCommand(
                            fitID=fitID, position=position, amount=cleanInput))


ChangeItemAmount.register()


class AmountChanger(wx.Dialog):

    def __init__(self, parent, value, limits=None):
        wx.Dialog.__init__(self, parent, title="Change Amount")
        self.SetMinSize((346, 156))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, "New Amount:" if limits is None else "New Amount ({}-{})".format(*limits))
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
