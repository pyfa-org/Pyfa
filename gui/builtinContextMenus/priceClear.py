from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.price import Price
from service.settings import ContextMenuSettings


class PriceClear(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('priceClear'):
            return False

        return srcContext in ("priceViewFull", "priceViewMinimal")

    def getText(self, itmContext, selection):
        return "Reset Price Cache"

    def activate(self, fullContext, selection, i):
        sPrc = Price.getInstance()
        sPrc.clearPriceCache()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))


PriceClear.register()
