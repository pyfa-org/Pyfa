from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.settings import ContextMenuSettings
import gui.fitCommands as cmd


class FillWithModule(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('moduleFill'):
            return False
        return srcContext in ("fittingModule")

    def getText(self, itmContext, selection):
        return u"Fill With {0}".format(itmContext if itmContext is not None else "Module")

    def activate(self, fullContext, selection, i):

        srcContext = fullContext[0]
        fitID = self.mainFrame.getActiveFit()

        if srcContext == "fittingModule":
            self.mainFrame.command.Submit(cmd.GuiFillWithModulesCommand(fitID, selection[0].itemID))
            return  # the command takes care of the PostEvent
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


FillWithModule.register()
