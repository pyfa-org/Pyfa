import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from eos.saveddata.module import Module
from logbook import Logger
pyfalog = Logger(__name__)
import eos.db

class FitSetChargeCommand(wx.Command):
    def __init__(self, fitID, modules, chargeID=None):
        # todo: determine if this command really should be used with a group of modules, or a simple per module basis
        wx.Command.__init__(self, True, "Module Charge Add")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.chargeID = chargeID
        self.modules = modules
        self.positions = {mod.modPosition: mod.chargeID for mod in modules}

    def Do(self):
        pyfalog.debug("Set ammo for fit ID: {0}", self.fitID)
        if self.fitID is None:
            return False
        return self.__setAmmo(self.modules, self.chargeID)

    def Undo(self):
        fit = eos.db.getFit(self.fitID)
        for position, chargeID in self.positions.items():
            self.__setAmmo([fit.modules[position]], chargeID)
        return True

    @staticmethod
    def __setAmmo(modules, chargeID):
        ammo = eos.db.getItem(chargeID) if chargeID else None
        result = False

        for mod in modules:
            if not mod.isEmpty and mod.isValidCharge(ammo):
                result = True
                mod.charge = ammo
        eos.db.commit()
        return result