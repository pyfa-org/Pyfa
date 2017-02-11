from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.market import Market


class PriceClear(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext == "priceViewFull"

    def getText(self, itmContext, selection):
        return "Reset Price Cache"

    def activate(self, fullContext, selection, i):
        sMkt = Market.getInstance()
        sMkt.clearPriceCache()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))


PriceClear.register()
