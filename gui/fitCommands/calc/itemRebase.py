import wx
from logbook import Logger

import eos.db
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class CalcRebaseItemCommand(wx.Command):

    def __init__(self, fitID, containerName, position, itemID, commit=True):
        wx.Command.__init__(self, True, 'Rebase Item')
        self.fitID = fitID
        self.containerName = containerName
        self.position = position
        self.itemID = itemID
        self.commit = commit
        self.savedItemID = None

    def Do(self):
        pyfalog.debug('Doing rebase of item in {} at position {} to {}'.format(self.containerName, self.position, self.itemID))
        fit = Fit.getInstance().getFit(self.fitID)
        obj = getattr(fit, self.containerName)[self.position]
        self.savedItemID = getattr(obj.item, 'ID', None)
        if self.savedItemID is None:
            pyfalog.warning('Unable to get old item ID')
            return False
        newItem = Market.getInstance().getItem(self.itemID)
        if newItem is None:
            pyfalog.warning('Unable to fetch new item')
            return False
        obj.rebase(newItem)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing rebase of item in {} at position {} to {}'.format(self.containerName, self.position, self.itemID))
        cmd = CalcRebaseItemCommand(
            fitID=self.fitID,
            containerName=self.containerName,
            position=self.position,
            itemID=self.savedItemID,
            commit=self.commit)
        return cmd.Do()
