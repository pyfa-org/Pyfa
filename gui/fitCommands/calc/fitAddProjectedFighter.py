import wx
import eos.db
from logbook import Logger
from eos.saveddata.fighter import Fighter
pyfalog = Logger(__name__)


class FitAddProjectedFighterCommand(wx.Command):
    """"
    from sFit.project
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.new_index = None

    def Do(self):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", self.fitID, self.itemID)
        fit = eos.db.getFit(self.fitID)
        item = eos.db.getItem(self.itemID, eager=("attributes", "group.category"))

        try:
            fighter = Fighter(item)
        except ValueError:
            return False

        fit.projectedFighters.append(fighter)
        # sometimes fighters aren't added because they aren't valid projectionable ones. todo: move that logic into here
        if fighter in fit.projectedFighters:
            eos.db.commit()
            self.new_index = fit.projectedFighters.index(fighter)
            return True
        return False

    def Undo(self):
        from gui.fitCommands.calc.fitRemoveProjectedFighter import FitRemoveProjectedFighterCommand  # avoids circular import
        cmd = FitRemoveProjectedFighterCommand(self.fitID, self.new_index)
        cmd.Do()
        return True
