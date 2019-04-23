# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from service.fit import Fit
from service.settings import ContextMenuSettings


class AmmoToDmgPattern(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('ammoPattern'):
            return False

        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        for attr in ("emDamage", "thermalDamage", "explosiveDamage", "kineticDamage"):
            if mainItem.getAttribute(attr) is not None:
                return True

        return False

    def getText(self, itmContext, mainItem, selection):
        return "Set {} as Damage Pattern".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, mainItem, selection, i):
        fitID = self.mainFrame.getActiveFit()
        Fit.getInstance().setAsPattern(fitID, mainItem)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def getBitmap(self, context, mainItem, selection):
        return None


AmmoToDmgPattern.register()
