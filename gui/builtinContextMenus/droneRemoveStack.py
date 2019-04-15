import math

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class ItemRemove(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('droneRemoveStack'):
            return False
        if srcContext not in ('droneItem', 'projectedDrone'):
            return False
        return True

    def getText(self, itmContext, selection):
        return "Remove {} Stack".format(itmContext)

    def activate(self, fullContext, selection, i):
        drone = selection[0]
        fitID = self.mainFrame.getActiveFit()
        if 'droneItem' in fullContext:
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalDroneCommand(
                fitID=fitID, position=Fit.getInstance().getFit(fitID).drones.index(drone), amount=math.inf))
        if 'projectedDrone' in fullContext:
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                fitID=fitID, itemID=drone.itemID, amount=math.inf))


ItemRemove.register()
