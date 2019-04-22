import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class FillWithModule(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('moduleFill'):
            return False
        return srcContext == "fittingModule"

    def getText(self, itmContext, mainItem, selection):
        return "Fill With {0}".format(itmContext if itmContext is not None else "Module")

    def activate(self, fullContext, mainItem, selection, i):

        srcContext = fullContext[0]
        fitID = self.mainFrame.getActiveFit()

        if srcContext == "fittingModule":
            fit = Fit.getInstance().getFit(fitID)
            if mainItem in fit.modules:
                position = fit.modules.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiFillWithClonedLocalModulesCommand(
                    fitID=fitID, position=position))


FillWithModule.register()
