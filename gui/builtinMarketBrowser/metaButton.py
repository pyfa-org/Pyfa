import wx
from logbook import Logger

pyfalog = Logger(__name__)


class MetaButton(wx.ToggleButton):
    def __init__(self, *args, **kwargs):
        super(MetaButton, self).__init__(*args, **kwargs)
        self.setUserSelection(True)

    def setUserSelection(self, isSelected):
        self.userSelected = isSelected
        self.SetValue(isSelected)

    def setMetaAvailable(self, isAvailable):
        self.Enable(isAvailable)
        # need to also SetValue(False) for windows because Enabled=False AND SetValue(True) looks enabled.
        if not isAvailable:
            self.SetValue(False)

    def reset(self):
        self.Enable(True)
        self.SetValue(self.userSelected)
