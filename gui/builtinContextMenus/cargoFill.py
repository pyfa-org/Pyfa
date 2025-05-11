import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class FillCargoWithItem(ContextMenuSingle):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc"):
            return False

        if mainItem is None:
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        # Only allow items that can be stored in cargo
        if not (mainItem.isCharge or mainItem.isCommodity):
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Fill Cargo With {0}").format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        
        # Get the item's volume
        itemVolume = mainItem.attributes['volume'].value
        if itemVolume is None or itemVolume <= 0:
            return
            
        # Calculate how many items can fit in the cargo
        cargoCapacity = fit.ship.getModifiedItemAttr("capacity")
        currentCargoVolume = fit.cargoBayUsed
        availableVolume = cargoCapacity - currentCargoVolume
        
        if availableVolume <= 0:
            return
            
        # Calculate maximum amount that can fit
        maxAmount = int(availableVolume / itemVolume)
        if maxAmount <= 0:
            return
            
        # Add the items to cargo
        command = cmd.GuiAddCargoCommand(fitID=fitID, itemID=int(mainItem.ID), amount=maxAmount)
        if self.mainFrame.command.Submit(command):
            self.mainFrame.additionsPane.select("Cargo", focus=False)


FillCargoWithItem.register() 