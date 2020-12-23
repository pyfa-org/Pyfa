# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class AmmoToDmgPattern(ContextMenuSingle):
    visibilitySetting = 'ammoPattern'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        for attr in ("emDamage", "thermalDamage", "explosiveDamage", "kineticDamage"):
            if mainItem.getAttribute(attr) is not None:
                return True

        return False

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Set {} as Damage Pattern").format(itmContext if itmContext is not None else _t("Item"))

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        Fit.getInstance().setAsPattern(fitID, mainItem)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def getBitmap(self, callingWindow, context, mainItem):
        return None


AmmoToDmgPattern.register()
