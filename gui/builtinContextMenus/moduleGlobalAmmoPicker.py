# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
import gui.mainFrame
import wx
from gui.bitmapLoader import BitmapLoader
from eos.types import Hardpoint
import gui.globalEvents as GE
from gui.builtinContextMenus.moduleAmmoPicker import ModuleAmmoPicker
import eos.db

class ModuleGlobalAmmoPicker(ModuleAmmoPicker):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

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
        fit = eos.db.getFit(fitID)

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
        try:
            selectionLen = len(selection)
        except:
            pass
        else:
            if selectionLen != 1:
                return False

        return super(ModuleGlobalAmmoPicker, self).display(srcContext, selection)


ModuleGlobalAmmoPicker.register()
