from abc import ABCMeta, abstractmethod

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import MarketPriceSettings


class ItemGroupPrice(ContextMenuUnconditional, metaclass=ABCMeta):

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

    def display(self, callingWindow, srcContext):
        return srcContext in ("priceViewFull", "priceViewMinimal")

    def getText(self, callingWindow, itmContext):
        return self.label

    def activate(self, callingWindow, fullContext, i):
        self.settings.set(self.optionName, not self.settings.get(self.optionName))
        fitID = self.mainFrame.getActiveFit()
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))

    def isChecked(self, i):
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
