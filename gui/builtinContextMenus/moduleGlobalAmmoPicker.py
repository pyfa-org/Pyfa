# -*- coding: utf-8 -*-
import gui.fitCommands as cmd
import gui.mainFrame
from eos.db.saveddata.queries import getFit as db_getFit
# noinspection PyPackageRequirements
from gui.builtinContextMenus.moduleAmmoPicker import ModuleAmmoPicker
from service.settings import ContextMenuSettings


class ModuleGlobalAmmoPicker(ModuleAmmoPicker):
    def __init__(self):
        super(ModuleGlobalAmmoPicker, self).__init__()
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
        fit = db_getFit(fitID)

        selectedModule = self.modules[0]
        allModules = []
        for mod in fit.modules:
            if mod.itemID is None:
                continue
            if mod.itemID == selectedModule.itemID:
                allModules.append(mod)

        self.mainFrame.command.Submit(cmd.GuiModuleAddChargeCommand(fitID, charge.ID if charge is not None else None, allModules))

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

        return super(ModuleGlobalAmmoPicker, self).display(srcContext, selection)


ModuleGlobalAmmoPicker.register()
