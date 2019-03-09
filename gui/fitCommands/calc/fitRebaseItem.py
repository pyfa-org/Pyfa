import wx

from logbook import Logger

import eos.db


pyfalog = Logger(__name__)


class FitRebaseItemCommand(wx.Command):

    def __init__(self, fitID, containerName, position, newTypeID):
        wx.Command.__init__(self, True, "Rebase Item")
        self.fitID = fitID
        self.containerName = containerName
        self.position = position
        self.newTypeID = newTypeID
        self.oldTypeID = None

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        obj = getattr(fit, self.containerName)[self.position]
        self.oldTypeID = getattr(obj.item, "ID", None)
        newItem = eos.db.getItem(self.newTypeID)
        obj.rebase(newItem)
        return True

    def Undo(self):
        cmd = FitRebaseItemCommand(self.fitID, self.containerName, self.position, self.oldTypeID)
        return cmd.Do()
