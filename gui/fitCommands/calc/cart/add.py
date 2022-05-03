import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddCartCommand(wx.Command):

    def __init__(self, fitID, cartInfo):
        wx.Command.__init__(self, True, 'Add Cart')
        self.fitID = fitID
        self.cartInfo = cartInfo

    def Do(self):
        pyfalog.debug('Doing addition of cart {} to fit {}'.format(self.cartInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        cart = next((c for c in fit.cart if c.itemID == self.cartInfo.itemID), None)
        if cart is not None:
            cart.amount += self.cartInfo.amount
        else:
            cart = self.cartInfo.toCart()
            fit.cart.append(cart)
            if cart not in fit.cart:
                pyfalog.warning('Failed to append to list')
                return False
        return True

    def Undo(self):
        pyfalog.debug('Undoing addition of cart {} to fit {}'.format(self.cartInfo, self.fitID))
        from .remove import CalcRemoveCartCommand
        cmd = CalcRemoveCartCommand(fitID=self.fitID, cartInfo=self.cartInfo)
        return cmd.Do()
