from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.fittingView
import wx
import gui.fittingView
from gui import bitmapLoader

class AmmoPattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()


    def display(self, context, selection):
        if context not in ("item", "itemSearch") or self.mainFrame.getActiveFit() is None:
            return False

        item = selection[0]
        if context == "itemSearch":
            item = service.Market.getInstance().getItem(item.ID)

        for attr in ("emDamage", "thermalDamage", "explosiveDamage", "kineticDamage"):
            if item.getAttribute(attr) is not None:
                return True

        return False

    def getText(self, context, selection):
        return "Set as damage pattern"

    def activate(self, context, selection, i):
        item = selection[0]
        if context == "itemSearch":
            item = service.Market.getInstance().getItem(item.ID)

        fit = self.mainFrame.getActiveFit()
        sFit = service.Fit.getInstance()
        sFit.setAsPattern(fit, item)
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fit))

    def getBitmap(self, context, selection):
        return None


AmmoPattern.register()
