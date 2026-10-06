# noinspection PyPackageRequirements
import wx

from eos.saveddata.module import Module
from eos.saveddata.drone import Drone
from gui.viewColumn import ViewColumn


class Omega(ViewColumn):
    name = "Omega"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.size = 20
        self.mask = wx.LIST_MASK_IMAGE
        self.columnText = "\u03A9"

    def getImageId(self, stuff):
        if isinstance(stuff, (Module, Drone)):
            if stuff.isEmpty:
                return -1
            item = stuff.item
        else:
            item = getattr(stuff, "item", stuff)
        if item is None:
            return -1
        if item.getAttribute("cloneGradeRestriction", 0) > 0:
            return self.fittingView.imageList.GetImageIndex(25874, "icons")
        return -1


Omega.register()
