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
        sMkt = service.Market.getInstance()
        if selection is None or len(selection) < 1:
            return False
        item = getattr(selection[0], "item", selection[0])
        doit =  srcContext in validContexts and (not selection[0].isEmpty if srcContext == "fittingModule" else True) \
        and sMkt.getMarketGroupByItem(item) is not None
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
