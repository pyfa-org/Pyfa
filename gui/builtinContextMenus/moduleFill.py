import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit


class FillWithModule(ContextMenuSingle):

    visibilitySetting = 'moduleFill'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if mainItem is None or getattr(mainItem, 'isEmpty', False):
            return False

        return srcContext == "fittingModule"

    def getText(self, callingWindow, itmContext, mainItem):
        return "Fill With {0}".format(itmContext if itmContext is not None else "Module")

    def activate(self, callingWindow, fullContext, mainItem, i):

        srcContext = fullContext[0]
        fitID = self.mainFrame.getActiveFit()

        if srcContext == "fittingModule":
            fit = Fit.getInstance().getFit(fitID)
            if mainItem in fit.modules:
                position = fit.modules.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiFillWithClonedLocalModulesCommand(
                    fitID=fitID, position=position))


FillWithModule.register()
