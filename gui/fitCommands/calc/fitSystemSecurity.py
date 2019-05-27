import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeFitSystemSecurityCommand(wx.Command):

    def __init__(self, fitID, secStatus):
        wx.Command.__init__(self, True, 'Change Fit System Security')
        self.fitID = fitID
        self.secStatus = secStatus
        self.savedSecStatus = None

    def Do(self):
        pyfalog.debug('Doing changing system security status of fit {} to {}'.format(self.fitID, self.secStatus))
        fit = Fit.getInstance().getFit(self.fitID, basic=True)
        # Fetching status via getter and then saving 'raw' security status
        # is intentional, to restore pre-change state properly
        if fit.getSystemSecurity() == self.secStatus:
            return False
        self.savedSecStatus = fit.systemSecurity
        fit.systemSecurity = self.secStatus
        return True

    def Undo(self):
        pyfalog.debug('Undoing changing system security status of fit {} to {}'.format(self.fitID, self.secStatus))
        cmd = CalcChangeFitSystemSecurityCommand(fitID=self.fitID, secStatus=self.savedSecStatus)
        return cmd.Do()
