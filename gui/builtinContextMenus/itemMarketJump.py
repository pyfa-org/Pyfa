import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.market import Market
from service.settings import ContextMenuSettings


class JumpToMarketItem(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        validContexts = ("marketItemMisc", "fittingModule",
                         "fittingCharge", "droneItem",
                         "implantItem", "boosterItem",
                         "projectedModule", "projectedDrone",
                         "projectedCharge", "cargoItem",
                         "implantItemChar", "fighterItem",
                         "projectedFighter")

        if srcContext not in validContexts or mainItem is None:
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

    def getText(self, itmContext, mainItem, selection):
        return "{0} Market Group".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, mainItem, selection, i):
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
