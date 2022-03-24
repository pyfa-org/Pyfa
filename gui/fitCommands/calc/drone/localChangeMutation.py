import wx
from logbook import Logger

from service.fit import Fit


pyfalog = Logger(__name__)


class CalcChangeLocalDroneMutationCommand(wx.Command):

    def __init__(self, fitID, position, mutation, oldMutation=None):
        wx.Command.__init__(self, True, 'Change Local Drone Mutation')
        self.fitID = fitID
        self.position = position
        self.mutation = mutation
        self.savedMutation = oldMutation

    def Do(self):
        pyfalog.debug('Doing changing of local drone mutation at position {} to {} for fit ID {}'.format(
            self.position, self.mutation, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        drone = fit.drones[self.position]
        if not drone.isMutated:
            return False

        if self.savedMutation is None:
            self.savedMutation = {}
            for mutator in drone.mutators.values():
                self.savedMutation[mutator.attrID] = mutator.value

        if self.mutation == self.savedMutation:
            return False

        for mutator in drone.mutators.values():
            if mutator.attrID not in self.mutation:
                continue
            if mutator.value != self.mutation[mutator.attrID]:
                mutator.value = self.mutation[mutator.attrID]

        return True

    def Undo(self):
        pyfalog.debug('Undoing changing of local drone mutation at position {} to {} for fit ID {}'.format(
            self.position, self.mutation, self.fitID))
        cmd = CalcChangeLocalDroneMutationCommand(
            fitID=self.fitID,
            position=self.position,
            mutation=self.savedMutation)
        return cmd.Do()
