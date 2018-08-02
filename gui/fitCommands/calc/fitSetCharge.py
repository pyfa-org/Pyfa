import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from eos.saveddata.module import Module
from logbook import Logger
pyfalog = Logger(__name__)
import eos.db

class FitSetChargeCommand(wx.Command):
    def __init__(self, fitID, positions, chargeID=None):
        # todo: determine if this command really should be used with a group of modules, or a simple per module basis
        wx.Command.__init__(self, True, "Module Charge Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.chargeID = chargeID
        self.positions = positions
        self.cache = None

    def Do(self):
        pyfalog.debug("Set ammo for fit ID: {0}", self.fitID)
        return self.__setAmmo(self.positions, self.chargeID)

    def Undo(self):
        for position, chargeID in self.cache.items():
            self.__setAmmo([position], chargeID)
        return True

    def __setAmmo(self, positions, chargeID):
        fit = eos.db.getFit(self.fitID)
        self.cache = {fit.modules[i].modPosition: fit.modules[i].chargeID for i in positions}
        ammo = eos.db.getItem(chargeID) if chargeID else None

        if not ammo.isCharge:
            return False
        result = False

        for pos in positions:
            mod = fit.modules[pos]
            if not mod.isEmpty and mod.isValidCharge(ammo):
                result = True
                mod.charge = ammo
        eos.db.commit()
        return result