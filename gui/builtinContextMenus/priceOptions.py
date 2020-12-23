from abc import ABCMeta, abstractmethod

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import MarketPriceSettings

_t = wx.GetTranslation


class ItemGroupPrice(ContextMenuUnconditional, metaclass=ABCMeta):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = MarketPriceSettings.getInstance()

    @property
    @abstractmethod
    def optionName(self):
        raise NotImplementedError()

    def display(self, callingWindow, srcContext):
        return srcContext in ("priceViewFull", "priceViewMinimal")

    def activate(self, callingWindow, fullContext, i):
        self.settings.set(self.optionName, not self.settings.get(self.optionName))
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def isChecked(self, i):
        return self.settings.get(self.optionName)


class DronesPrice(ItemGroupPrice):
    optionName = 'drones'

    def getText(self, callingWindow, itmContext):
        return _t('Drones')


class CargoPrice(ItemGroupPrice):
    optionName = 'cargo'

    def getText(self, callingWindow, itmContext):
        return _t('Cargo')


class ImplantBoosterPrice(ItemGroupPrice):
    optionName = 'character'

    def getText(self, callingWindow, itmContext):
        return _t('Implants && Boosters')


DronesPrice.register()
CargoPrice.register()
ImplantBoosterPrice.register()
