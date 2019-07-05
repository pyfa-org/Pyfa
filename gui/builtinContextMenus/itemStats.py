# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from gui.itemStats import ItemStatsDialog
from service.fit import Fit


class ItemStats(ContextMenuSingle):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, mainItem):
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

    def getText(self, itmContext, mainItem):
        return "{} Stats".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, mainItem, i):
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

        mstate = wx.GetMouseState()
        reuse = False

        if mstate.GetModifiers() == wx.MOD_SHIFT:
            reuse = True

        if self.mainFrame.GetActiveStatsWindow() is None and reuse:
            ItemStatsDialog(stuff, fullContext)

        elif reuse:
            lastWnd = self.mainFrame.GetActiveStatsWindow()
            pos = lastWnd.GetPosition()
            maximized = lastWnd.IsMaximized()
            if not maximized:
                size = lastWnd.GetSize()
            else:
                size = wx.DefaultSize
                pos = wx.DefaultPosition
            ItemStatsDialog(stuff, fullContext, pos, size, maximized)
            lastWnd.Close()

        else:
            ItemStatsDialog(stuff, fullContext)


ItemStats.register()
