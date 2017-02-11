from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.fit import Fit


class AmmoPattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        item = selection[0]
        for attr in ("emDamage", "thermalDamage", "explosiveDamage", "kineticDamage"):
            if item.getAttribute(attr) is not None:
                return True

        return False

    def getText(self, itmContext, selection):
        return "Set {0} as Damage Pattern".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):
        item = selection[0]
        fit = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        sFit.setAsPattern(fit, item)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fit))

    def getBitmap(self, context, selection):
        return None


AmmoPattern.register()
