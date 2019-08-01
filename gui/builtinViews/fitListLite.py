# noinspection PyPackageRequirements
import wx

import gui.display as d


class FitListView(d.Display):

    DEFAULT_COLS = ['Base Name']

    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self.fits = []

    def updateView(self):
        self.update(self.fits)

    def refreshView(self):
        self.refresh(self.fits)

    def updateData(self, fits):
        fits.sort(key=lambda f: (f.shipName, f.name))
        self.fits = fits
        self.updateView()
