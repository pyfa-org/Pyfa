import wx
import eos.db
from logbook import Logger
from eos.saveddata.implant import Implant
pyfalog = Logger(__name__)


class FitAddImplantCommand(wx.Command):
    """"
    from sFit.addImplant
    """
    def __init__(self, fitID, itemID, state):
        wx.Command.__init__(self, True, "Add Implant")
        self.fitID = fitID
        self.newItemID = itemID
        self.newState = state
        self.newIndex = None
        self.oldItemID = None
        self.oldState = None

    def Do(self):
        pyfalog.debug("Adding implant to fit ({0}) for item ID: {1}", self.fitID, self.newItemID)

        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.newItemID, eager="attributes")

        if next((x for x in fit.implants if x.itemID == self.newItemID), None):
            return False  # already have item in list of implants

        try:
            implant = Implant(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", self.newItemID)
            return False
        implant.active = self.newState
        
        self.oldItemID, self.oldState = fit.implants.makeRoom(implant)
        fit.implants.append(implant)
        self.newIndex = fit.implants.index(implant)
        return True

    def Undo(self):
        if self.oldItemID:
            # If we had an item in the slot previously, add it back.
            cmd = FitAddImplantCommand(self.fitID, self.oldItemID, self.oldState)
            cmd.Do()
            return True

        from .fitRemoveImplant import FitRemoveImplantCommand  # Avoid circular import
        cmd = FitRemoveImplantCommand(self.fitID, self.newIndex)
        cmd.Do()
        return True
