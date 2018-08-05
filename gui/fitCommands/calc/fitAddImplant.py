import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
#from .helpers import ModuleInfoCache
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)
from eos.saveddata.implant import Implant

class FitAddImplantCommand(wx.Command):
    """"
    from sFit.addImplant
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Cargo add")
        self.fitID = fitID
        self.itemID = itemID
        self.old_item = None

    def Do(self):
        pyfalog.debug("Adding implant to fit ({0}) for item ID: {1}", self.fitID, self.itemID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager="attributes")
        try:
            implant = Implant(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", self.itemID)
            return False

        self.old_item = fit.implants.makeRoom(implant)
        fit.implants.append(implant)
        self.new_index = fit.implants.index(implant)
        return True

    def Undo(self):
        if self.old_item:
            # If we had an item in the slot previously, add it back.
            cmd = FitAddImplantCommand(self.fitID, self.old_item)
            cmd.Do()
            return True

        from .fitRemoveImplant import FitRemoveImplantCommand  # Avoid circular import
        cmd = FitRemoveImplantCommand(self.fitID, self.new_index)
        cmd.Do()
        return True
