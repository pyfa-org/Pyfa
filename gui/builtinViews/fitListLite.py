# noinspection PyPackageRequirements
import wx

import gui.display as d


class FitListView(d.Display):

    DEFAULT_COLS = ['Base Name']

    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
