from abc import ABCMeta, abstractmethod

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from service.settings import MarketPriceSettings


class ItemGroupPrice(ContextMenuCombined, metaclass=ABCMeta):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = MarketPriceSettings.getInstance()

    @property
    @abstractmethod
    def label(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def optionName(self):
        raise NotImplementedError()

    def display(self, srcContext, mainItem, selection):
        return srcContext in ("priceViewFull", "priceViewMinimal")

    def getText(self, itmContext, mainItem, selection):
        return self.label

    def activate(self, fullContext, mainItem, selection, i):
        self.settings.set(self.optionName, not self.settings.get(self.optionName))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    @property
    def checked(self):
        return self.settings.get(self.optionName)


class DronesPrice(ItemGroupPrice):

    label = 'Drones'
    optionName = 'drones'


class CargoPrice(ItemGroupPrice):

    label = 'Cargo'
    optionName = 'cargo'


class ImplantBoosterPrice(ItemGroupPrice):

    label = 'Implants && Boosters'
    optionName = 'character'


DronesPrice.register()
CargoPrice.register()
ImplantBoosterPrice.register()
