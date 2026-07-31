from wx import ProgressDialog
class ProgressHelper:

    def __init__(self, message, maximum=None, callback=None):
        #type: (str, int, function) -> None
        self.message = message
        self.current = 0
        self.maximum = maximum
        self.workerWorking = True # type: bool
        self.dlgWorking = True # type: bool
        self.error = None # type: str
        self.callback = callback
        self.cbArgs = [] # type: list[str]
        self.dlg = None # type: ProgressDialog

    def setRange(self, max):
        # type: (int) -> None
        """
        call ProgressDialog.SetRange(max)
        """
        self.maximum = max
        if (self.dlg):
            self.dlg.SetRange(max)

    # def pulse(self, msg):
    #     # type: (str) -> None
    #     if (self.dlg):
    #         self.dlgWorking, skip = self.dlg.Pulse(msg)

    # def update(self, value, msg):
    #     # type: (int, str) -> None
    #     if (self.dlg):
    #         self.dlgWorking, skip = self.dlg.Update(value, msg)

    @property
    def working(self):
        return self.workerWorking and self.dlgWorking and not self.error

    @property
    def userCancelled(self):
        return not self.dlgWorking
