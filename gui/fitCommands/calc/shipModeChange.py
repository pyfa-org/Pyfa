import wx
from logbook import Logger

from eos.saveddata.mode import Mode
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class CalcChangeShipModeCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Change Ship Mode')
        self.fitID = fitID
        self.itemID = itemID
        self.savedItemID = None

    def Do(self):
        pyfalog.debug('Doing changing ship mode to {} for fit {}'.format(self.itemID, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        self.savedItemID = fit.mode.item.ID
        item = Market.getInstance().getItem(self.itemID)
        mode = Mode(item)
        fit.mode = mode
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing ship mode to {} for fit {}'.format(self.itemID, self.fitID))
        cmd = CalcChangeShipModeCommand(self.fitID, self.savedItemID)
        return cmd.Do()
