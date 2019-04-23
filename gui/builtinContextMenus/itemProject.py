import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from service.fit import Fit
from service.settings import ContextMenuSettings


class ProjectItem(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('project'):
            return False

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

    def getText(self, itmContext, mainItem, selection):
        return "Project {0} onto Fit".format(itmContext)

    def activate(self, fullContext, mainItem, selection, i):
        fitID = self.mainFrame.getActiveFit()
        category = mainItem.category.name
        if category == 'Module':
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(fitID=fitID, itemID=mainItem.ID))
        elif category == 'Drone':
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedDroneCommand(fitID=fitID, itemID=mainItem.ID))
        elif category == 'Fighter':
            success = self.mainFrame.command.Submit(cmd.GuiAddProjectedFighterCommand(fitID=fitID, itemID=mainItem.ID))
        else:
            success = False
        if success:
            self.mainFrame.additionsPane.select('Projected')


ProjectItem.register()
