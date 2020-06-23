# noinspection PyPackageRequirements

import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from gui.itemStats import ItemStatsFrame
from service.fit import Fit

_t = wx.GetTranslation


class ItemStats(ContextMenuSingle):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in (
                "marketItemGroup", "marketItemMisc",
                "fittingModule", "fittingCharge",
                "fittingShip", "baseShip",
                "cargoItem", "droneItem",
                "implantItem", "boosterItem",
                "skillItem", "projectedModule",
                "projectedDrone", "projectedCharge",
                "itemStats", "fighterItem",
                "implantItemChar", "projectedFighter",
                "fittingMode"
        ):
            return False

        if (mainItem is None or getattr(mainItem, "isEmpty", False)) and srcContext != "fittingShip":
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("{} Stats").format(itmContext if itmContext is not None else _t("Item"))

    def activate(self, callingWindow, fullContext, mainItem, i):
        srcContext = fullContext[0]
        if srcContext == "fittingShip":
            fitID = self.mainFrame.getActiveFit()
            sFit = Fit.getInstance()
            stuff = sFit.getFit(fitID).ship
        elif srcContext == "fittingMode":
            stuff = mainItem.item
        else:
            stuff = mainItem

        if srcContext == "fittingModule" and stuff.isEmpty:
            return

        reuse = False

        if wx.GetMouseState().GetModifiers() == wx.MOD_SHIFT:
            reuse = True

        if self.mainFrame.GetActiveStatsWindow() is None and reuse:
            frame = ItemStatsFrame(stuff, fullContext)
        elif reuse:
            lastWnd = self.mainFrame.GetActiveStatsWindow()
            pos = lastWnd.GetPosition()
            maximized = lastWnd.IsMaximized()
            if not maximized:
                size = lastWnd.GetSize()
            else:
                size = wx.DefaultSize
                pos = wx.DefaultPosition
            frame = ItemStatsFrame(stuff, fullContext, pos, size, maximized)
            lastWnd.Close()

        else:
            frame = ItemStatsFrame(stuff, fullContext)
        frame.Show()


ItemStats.register()
