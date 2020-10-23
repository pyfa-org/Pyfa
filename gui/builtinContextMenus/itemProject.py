import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class ProjectItem(ContextMenuSingle):
    visibilitySetting = 'project'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if fit.isStructure:
            return False

        return mainItem.isType("projected")

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Project {0} onto Fit").format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        if mainItem.isModule:
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(fitID=fitID, itemID=mainItem.ID))
        elif mainItem.isDrone:
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedDroneCommand(fitID=fitID, itemID=mainItem.ID))
        elif mainItem.isFighter:
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedFighterCommand(fitID=fitID, itemID=mainItem.ID))
        else:
            success = False
        if success:
            self.mainFrame.additionsPane.select('Projected', focus=False)


ProjectItem.register()
