import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleImplantStateCommand(wx.Command):

    def __init__(self, fitID, position, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Implant State')
        self.fitID = fitID
        self.position = position
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of implant state at position {} for fit {}'.format(self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        implant = fit.implants[self.position]
        self.savedState = implant.active
        implant.active = not implant.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Undoing toggling of implant state at position {} for fit {}'.format(self.position, self.fitID))
        cmd = CalcToggleImplantStateCommand(fitID=self.fitID, position=self.position, forceState=self.savedState)
        return cmd.Do()
