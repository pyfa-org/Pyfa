# Borrowed from new eos


from utils.repr import makeReprStr


class CycleInfo:

    def __init__(self, activeTime, inactiveTime, quantity, isInactivityReload):
        self.activeTime = activeTime
        self.inactiveTime = inactiveTime
        self.quantity = quantity
        self.isInactivityReload = isInactivityReload

    @property
    def averageTime(self):
        return self.activeTime + self.inactiveTime

    def iterCycles(self):
        i = 0
        while i < self.quantity:
            yield self.activeTime, self.inactiveTime, self.isInactivityReload
            i += 1

    def _getCycleQuantity(self):
        return self.quantity

    def _getTime(self):
        return (self.activeTime + self.inactiveTime) * self.quantity

    def __repr__(self):
        spec = ['activeTime', 'inactiveTime', 'quantity', 'isInactivityReload']
        return makeReprStr(self, spec)


class CycleSequence:

    def __init__(self, sequence, quantity):
        self.sequence = sequence
        self.quantity = quantity

    @property
    def averageTime(self):
        """Get average time between cycles."""
        return self._getTime() / self._getCycleQuantity()

    def iterCycles(self):
        i = 0
        while i < self.quantity:
            for cycleInfo in self.sequence:
                for cycleTime, inactiveTime, isInactivityReload in cycleInfo.iterCycles():
                    yield cycleTime, inactiveTime, isInactivityReload
            i += 1

    def _getCycleQuantity(self):
        quantity = 0
        for item in self.sequence:
            quantity += item._getCycleQuantity()
        return quantity

    def _getTime(self):
        time = 0
        for item in self.sequence:
            time += item._getTime()
        return time

    def __repr__(self):
        spec = ['sequence', 'quantity']
        return makeReprStr(self, spec)
