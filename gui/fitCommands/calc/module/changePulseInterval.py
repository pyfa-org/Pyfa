import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeLocalModulePulseIntervalCommand(wx.Command):

    def __init__(self, fitID, positions, pulseInterval):
        wx.Command.__init__(self, True, 'Change Module Pulse Interval')
        self.fitID = fitID
        self.positions = positions
        self.pulseInterval = pulseInterval
        self.savedIntervals = {}

    def Do(self):
        pyfalog.debug('Doing change of module pulse interval on fit {} positions {} to {}'.format(
            self.fitID, self.positions, self.pulseInterval))
        fit = Fit.getInstance().getFit(self.fitID)
        positions = [pos for pos in self.positions if not fit.modules[pos].isEmpty]
        if len(positions) == 0:
            return False
        self.savedIntervals = {pos: fit.modules[pos].pulseInterval for pos in positions}
        changed = False
        for position in positions:
            mod = fit.modules[position]
            if mod.pulseInterval != self.pulseInterval:
                mod.pulseInterval = self.pulseInterval
                changed = True
        return changed

    def Undo(self):
        pyfalog.debug('Undoing change of module pulse interval on fit {} positions {} to {}'.format(
            self.fitID, self.positions, self.pulseInterval))
        fit = Fit.getInstance().getFit(self.fitID)
        for position, interval in self.savedIntervals.items():
            fit.modules[position].pulseInterval = interval
        return True
