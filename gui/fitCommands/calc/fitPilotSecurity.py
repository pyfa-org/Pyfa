import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeFitPilotSecurityCommand(wx.Command):

    def __init__(self, fitID, secStatus):
        wx.Command.__init__(self, True, 'Change Fit Pilot Security')
        self.fitID = fitID
        self.secStatus = secStatus
        self.savedSecStatus = None

    def Do(self):
        pyfalog.debug('Doing changing pilot security status of fit {} to {}'.format(self.fitID, self.secStatus))
        fit = Fit.getInstance().getFit(self.fitID, basic=True)
        # Fetching status via getter and then saving 'raw' security status
        # is intentional, to restore pre-change state properly
        if fit.pilotSecurity == self.secStatus:
            return False
        self.savedSecStatus = fit.pilotSecurity
        fit.pilotSecurity = self.secStatus
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing pilot security status of fit {} to {}'.format(self.fitID, self.secStatus))
        cmd = CalcChangeFitPilotSecurityCommand(fitID=self.fitID, secStatus=self.savedSecStatus)
        return cmd.Do()
