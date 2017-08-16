from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
from gui.builtinShipBrowser.events import FitSelected
from service.settings import ContextMenuSettings


class OpenFit(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('openFit'):
            return False

        return srcContext in ("projectedFit", "commandFit")

    def getText(self, itmContext, selection):
        return "Open Fit in New Tab"

    def activate(self, fullContext, selection, i):
        fit = selection[0]
        wx.PostEvent(self.mainFrame, FitSelected(fitID=fit.ID, startup=2))


OpenFit.register()
