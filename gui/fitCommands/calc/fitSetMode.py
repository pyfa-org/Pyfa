import wx
from logbook import Logger

import eos.db
from eos.saveddata.mode import Mode
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class FitSetModeCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Set Mode')
        self.fitID = fitID
        self.itemID = itemID
        self.savedItemID = None

    def Do(self):
        pyfalog.debug('Doing setting mode {} for fit {}'.format(self.itemID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        self.savedItemID = fit.modeID
        item = Market.getInstance().getItem(self.itemID)
        mode = Mode(item)
        fit.mode = mode
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitSetModeCommand(self.fitID, self.savedItemID)
        return cmd.Do()
