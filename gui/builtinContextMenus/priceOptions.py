from abc import abstractmethod, ABCMeta

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.settings import MarketPriceSettings


class ItemGroupPrice(ContextMenu, metaclass=ABCMeta):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = MarketPriceSettings.getInstance()

    @property
    @abstractmethod
    def label(self):
        ...

    @property
    @abstractmethod
    def optionName(self):
        ...

    def display(self, srcContext, selection):
        return srcContext in ("priceViewFull", "priceViewMinimal")

    def getText(self, itmContext, selection):
        return self.label

    def activate(self, fullContext, selection, i):
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
