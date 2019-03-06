import wx


class GuiOptimizePriceCommand(wx.Command):
    def __init__(self):
        wx.Command.__init__(self, True, "Optimize Price")

    def Do(self):
        pass

    def Undo(self):
        pass
