import wx
from logbook import Logger

from gui.fitCommands.helpers import CartInfo
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcRemoveCartCommand(wx.Command):

    def __init__(self, fitID, cartInfo):
        wx.Command.__init__(self, True, 'Remove Cart')
        self.fitID = fitID
        self.cartInfo = cartInfo
        self.savedRemovedAmount = None

    def Do(self):
        pyfalog.debug('Doing removal of cart {} to fit {}'.format(self.cartInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cart = next((x for x in fit.cart if x.itemID == self.cartInfo.itemID), None)
        if cart is None:
            return False
        self.savedRemovedAmount = min(cart.amount, self.cartInfo.amount)
        cart.amount -= self.savedRemovedAmount
        if cart.amount <= 0:
            fit.cart.remove(cart)
        return True

    def Undo(self):
        pyfalog.debug('Undoing removal of cart {} to fit {}'.format(self.cartInfo, self.fitID))
        from .add import CalcAddCartCommand
        cmd = CalcAddCartCommand(
            fitID=self.fitID,
            cartInfo=CartInfo(itemID=self.cartInfo.itemID, amount=self.savedRemovedAmount))
        return cmd.Do()
