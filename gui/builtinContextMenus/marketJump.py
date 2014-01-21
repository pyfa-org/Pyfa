from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class MarketJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        validContexts = ("marketItemMisc", "fittingModule", "fittingCharge", "droneItem", "implantItem",
                         "boosterItem", "projectedModule", "projectedDrone", "projectedCharge")
        if not srcContext in validContexts:
            return False
        sMkt = service.Market.getInstance()
        if selection is None or len(selection) < 1:
            return False
        item = getattr(selection[0], "item", selection[0])
        mktGrp = sMkt.getMarketGroupByItem(item)
        # 1663 is Special Edition Festival Assets, we don't have root group for it
        if mktGrp is None or mktGrp.ID == 1663:
            return False
        doit =  not selection[0].isEmpty if srcContext == "fittingModule" else True
        return doit

    def getText(self, itmContext, selection):
        return "{0} Market Group".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        if srcContext in ("fittingModule", "droneItem", "implantItem", "boosterItem", "projectedModule", "projectedDrone"):
            item = selection[0].item
        elif srcContext in ("fittingCharge", "projectedCharge"):
            item = selection[0].charge
        else:
            item = selection[0]

        self.mainFrame.notebookBrowsers.SetSelection(0)
        self.mainFrame.marketBrowser.jump(item)

MarketJump.register()
