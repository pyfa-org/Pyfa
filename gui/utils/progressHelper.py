class ProgressHelper:

    def __init__(self, message, maximum=None, callback=None):
        self.message = message
        self.current = 0
        self.maximum = maximum
        self.workerWorking = True
        self.dlgWorking = True
        self.error = None
        self.callback = callback
        self.cbArgs = []

    @property
    def working(self):
        return self.workerWorking and self.dlgWorking and not self.error

    @property
    def userCancelled(self):
        return not self.dlgWorking
