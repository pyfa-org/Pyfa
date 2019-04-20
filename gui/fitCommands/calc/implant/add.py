import wx
from logbook import Logger

import eos.db
from eos.exception import HandledListActionError
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcAddImplantCommand(wx.Command):

    def __init__(self, fitID, implantInfo, position=None, commit=True):
        wx.Command.__init__(self, True, 'Add Implant')
        self.fitID = fitID
        self.newImplantInfo = implantInfo
        self.newPosition = position
        self.commit = commit
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
            try:
                fit.implants.insert(self.newPosition, newImplant)
            except HandledListActionError:
                pyfalog.warning('Failed to insert to list')
                cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=self.oldImplantInfo, position=self.oldPosition)
                cmd.Do()
                return False
        else:
            try:
                fit.implants.append(newImplant)
            except HandledListActionError:
                pyfalog.warning('Failed to append to list')
                cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=self.oldImplantInfo, position=self.oldPosition)
                cmd.Do()
                return False
            self.newPosition = fit.implants.index(newImplant)
        if self.commit:
            eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undo addition of implant {} to fit {}'.format(self.newImplantInfo, self.fitID))
        if self.oldImplantInfo is not None and self.oldPosition is not None:
            cmd = CalcAddImplantCommand(
                fitID=self.fitID,
                implantInfo=self.oldImplantInfo,
                position=self.oldPosition,
                commit=self.commit)
            return cmd.Do()
        from .remove import CalcRemoveImplantCommand
        cmd = CalcRemoveImplantCommand(fitID=self.fitID, position=self.newPosition, commit=self.commit)
        return cmd.Do()
