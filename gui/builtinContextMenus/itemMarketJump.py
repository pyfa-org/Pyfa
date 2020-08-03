import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.market import Market

_t = wx.GetTranslation


class JumpToMarketItem(ContextMenuSingle):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        validContexts = ("marketItemMisc", "fittingModule",
                         "fittingCharge", "droneItem",
                         "implantItem", "boosterItem",
                         "projectedModule", "projectedDrone",
                         "projectedCharge", "cargoItem",
                         "implantItemChar", "fighterItem",
                         "projectedFighter")

        if srcContext not in validContexts or mainItem is None:
            return False

        if mainItem is None or getattr(mainItem, "isEmpty", False):
            return False

        sMkt = Market.getInstance()
        item = getattr(mainItem, "item", mainItem)
        isMutated = getattr(mainItem, "isMutated", False)
        mktGrp = sMkt.getMarketGroupByItem(item)
        if mktGrp is None and isMutated:
            mktGrp = sMkt.getMarketGroupByItem(mainItem.baseItem)

        # 1663 is Special Edition Festival Assets, we don't have root group for it
        if mktGrp is None or mktGrp.ID == 1663:
            return False

        doit = not mainItem.isEmpty if srcContext == "fittingModule" else True
        return doit

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("{0} Market Group").format(itmContext if itmContext is not None else _t("Item"))

    def activate(self, callingWindow, fullContext, mainItem, i):
        srcContext = fullContext[0]
        if srcContext in ("fittingCharge", "projectedCharge"):
            item = mainItem.charge
        elif hasattr(mainItem, "item"):
            if getattr(mainItem, "isMutated", False):
                item = mainItem.baseItem
            else:
                item = mainItem.item
        else:
            item = mainItem

        self.mainFrame.notebookBrowsers.SetSelection(0)
        self.mainFrame.marketBrowser.jump(item)


JumpToMarketItem.register()
