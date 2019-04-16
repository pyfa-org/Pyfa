import gui.fitCommands as cmd
import gui.mainFrame
from gui.builtinContextMenus.moduleAmmoChange import ChangeModuleAmmo
from service.fit import Fit
from service.settings import ContextMenuSettings


class ChangeModuleAmmoAll(ChangeModuleAmmo):

    def __init__(self):
        super(ChangeModuleAmmoAll, self).__init__()
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def getText(self, itmContext, selection):
        return "Charge (All)"

    def handleAmmoSwitch(self, event):
        if len(self.modules) != 1:
            event.Skip()
            return

        charge = self.chargeIds.get(event.Id, False)
        if charge is False:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        selectedModule = self.modules[0]
        if self.context == 'fittingModule':
            self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleChargesCommand(
                fitID=fitID,
                modules=[m for m in fit.modules if m.itemID is not None and m.itemID == selectedModule.itemID],
                chargeItemID=charge.ID if charge is not None else None))
        elif self.context == 'projectedModule':
            self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleChargesCommand(
                fitID=fitID,
                modules=[m for m in fit.projectedModules if m.itemID is not None and m.itemID == selectedModule.itemID],
                chargeItemID=charge.ID if charge is not None else None))

    def display(self, srcContext, selection):
        if not self.settings.get('moduleGlobalAmmoPicker'):
            return False

        try:
            selectionLen = len(selection)
        except:
            pass
        else:
            if selectionLen != 1:
                return False

        return super(ChangeModuleAmmoAll, self).display(srcContext, selection)


ChangeModuleAmmoAll.register()
