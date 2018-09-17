import wx
from logbook import Logger

import eos.db

pyfalog = Logger(__name__)


class FitRemoveFighterCommand(wx.Command):
    """"
    Fitting command that removes a module at a specified positions

    from sFit.removeFighter
    """
    def __init__(self, fitID: int, position: int):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.position = position
        self.change = None
        self.removed_item = None

    def Do(self):
        fitID = self.fitID
        fit = eos.db.getFit(fitID)
        f = fit.fighters[self.position]
        fit.fighters.remove(f)
        self.removed_item = f.itemID
        eos.db.commit()
        return True

    def Undo(self):
        from gui.fitCommands.calc.fitAddFighter import FitAddFighterCommand  # avoids circular import
        cmd = FitAddFighterCommand(self.fitID, self.removed_item)
        return cmd.Do()
