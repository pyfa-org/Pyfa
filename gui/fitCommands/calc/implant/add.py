import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddImplantCommand(wx.Command):

    def __init__(self, fitID, implantInfo, position=None):
        wx.Command.__init__(self, True, 'Add Implant')
        self.fitID = fitID
        self.newImplantInfo = implantInfo
        self.newPosition = position
        self.oldImplantInfo = None
        self.oldPosition = None

    def Do(self):
        pyfalog.debug('Doing addition of implant {} to fit {}'.format(self.newImplantInfo, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)

        if any(self.newImplantInfo.itemID == i.itemID for i in fit.implants):
            pyfalog.debug('Skipping as such implant is already on the fit')
            return False

        newImplant = self.newImplantInfo.toImplant()
        if newImplant is None:
            return False

        self.oldPosition, self.oldImplantInfo = fit.implants.makeRoom(newImplant)

        if self.newPosition is not None:
            fit.implants.insert(self.newPosition, newImplant)
            if newImplant not in fit.implants:
                pyfalog.warning('Failed to insert to list')
                cmd = CalcAddImplantCommand(
                    fitID=self.fitID,
                    implantInfo=self.oldImplantInfo,
                    position=self.oldPosition)
                cmd.Do()
                return False
        else:
            fit.implants.append(newImplant)
            if newImplant not in fit.implants:
                pyfalog.warning('Failed to append to list')
                cmd = CalcAddImplantCommand(
                    fitID=self.fitID,
                    implantInfo=self.oldImplantInfo,
                    position=self.oldPosition)
                cmd.Do()
                return False
            self.newPosition = fit.implants.index(newImplant)
        return True

    def Undo(self):
        pyfalog.debug('Undo addition of implant {} to fit {}'.format(self.newImplantInfo, self.fitID))
        if self.oldImplantInfo is not None and self.oldPosition is not None:
            cmd = CalcAddImplantCommand(
                fitID=self.fitID,
                implantInfo=self.oldImplantInfo,
                position=self.oldPosition)
            return cmd.Do()
        from .remove import CalcRemoveImplantCommand
        cmd = CalcRemoveImplantCommand(fitID=self.fitID, position=self.newPosition)
        return cmd.Do()
