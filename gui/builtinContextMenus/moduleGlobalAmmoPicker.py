# -*- coding: utf-8 -*-
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from gui.builtinContextMenus.moduleAmmoPicker import ModuleAmmoPicker
from eos.db.saveddata.queries import getFit as db_getFit
from service.fit import Fit
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

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = db_getFit(fitID)

        selectedModule = self.modules[0]
        allModules = []
        for mod in fit.modules:
            if mod.itemID is None:
                continue
            if mod.itemID == selectedModule.itemID:
                allModules.append(mod)

        sFit.setAmmo(fitID, charge.ID if charge is not None else None, allModules)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

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
