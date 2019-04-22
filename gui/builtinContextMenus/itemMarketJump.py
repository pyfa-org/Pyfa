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

        if srcContext not in validContexts or selection is None or len(selection) < 1:
            return False

        sMkt = Market.getInstance()
        item = getattr(selection[0], "item", selection[0])
        isMutated = getattr(selection[0], "isMutated", False)
        mktGrp = sMkt.getMarketGroupByItem(item)
        if mktGrp is None and isMutated:
            mktGrp = sMkt.getMarketGroupByItem(selection[0].baseItem)

        # 1663 is Special Edition Festival Assets, we don't have root group for it
        if mktGrp is None or mktGrp.ID == 1663:
            return False

        doit = not selection[0].isEmpty if srcContext == "fittingModule" else True
        return doit

    def getText(self, itmContext, mainItem, selection):
        return "{0} Market Group".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, mainItem, selection, i):
        srcContext = fullContext[0]
        if srcContext in ("fittingCharge", "projectedCharge"):
            item = selection[0].charge
        elif hasattr(selection[0], "item"):
            if getattr(selection[0], "isMutated", False):
                item = selection[0].baseItem
            else:
                item = selection[0].item
        else:
            item = selection[0]

        self.mainFrame.notebookBrowsers.SetSelection(0)
        self.mainFrame.marketBrowser.jump(item)


JumpToMarketItem.register()
