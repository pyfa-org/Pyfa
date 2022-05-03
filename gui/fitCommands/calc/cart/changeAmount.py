import wx
from logbook import Logger

from gui.fitCommands.helpers import CartInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeCartAmountCommand(wx.Command):

    def __init__(self, fitID, cartInfo):
        wx.Command.__init__(self, True, 'Change Cart Amount')
        self.fitID = fitID
        self.cartInfo = cartInfo
        self.savedCartInfo = None

    def Do(self):
        pyfalog.debug('Doing change of cart {} for fit {}'.format(self.cartInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cart = next((c for c in fit.cart if c.itemID == self.cartInfo.itemID), None)
        if cart is None:
            pyfalog.warning('Cannot find cart item')
            return False
        self.savedCartInfo = CartInfo.fromCart(cart)
        if self.cartInfo.amount == self.savedCartInfo.amount:
            return False
        cart.amount = self.cartInfo.amount
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of cart {} for fit {}'.format(self.cartInfo, self.fitID))
        cmd = CalcChangeCartAmountCommand(fitID=self.fitID, cartInfo=self.savedCartInfo)
        return cmd.Do()
