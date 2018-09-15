import wx
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitChangeProjectedFitQty(wx.Command):
    """"
    from sFit.changeAmount
    """
    def __init__(self, fitID, pfitID, amount=1):
        wx.Command.__init__(self, True, "Drone add")
        self.fitID = fitID
        self.pfitID = pfitID
        self.amount = amount
        self.old_amount = None

    def Do(self):
        pfit = eos.db.getFit(self.pfitID)

        if not pfit:  # fit was deleted
            return False

        amount = min(20, max(1, self.amount))  # 1 <= a <= 20

        projectionInfo = pfit.getProjectionInfo(self.fitID)
        if projectionInfo:
            self.old_amount = projectionInfo.amount
            projectionInfo.amount = amount

        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitChangeProjectedFitQty(self.fitID, self.pfitID, self.old_amount)
        return cmd.Do()
