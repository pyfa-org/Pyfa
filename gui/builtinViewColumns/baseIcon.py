from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
from gui.bitmapLoader import BitmapLoader
import wx
from eos.types import Drone, Fit, Module, Slot, Rack

class BaseIcon(ViewColumn):
    name = "Base Icon"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.size = 24
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_IMAGE
        self.columnText = ""
        self.shipImage = fittingView.imageList.GetImageIndex("ship_small", "gui")

    def getImageId(self, stuff):
        if isinstance(stuff, Drone):
            return -1
        if isinstance(stuff, Fit):
            return self.shipImage
        if isinstance(stuff, Rack):
            return -1
        if isinstance(stuff, Module):
            if stuff.isEmpty:
                return self.fittingView.imageList.GetImageIndex("slot_%s_small" % Slot.getName(stuff.slot).lower(), "gui")
            else:
                return self.loadIconFile(stuff.item.icon.iconFile if stuff.item.icon else "")

        item = getattr(stuff, "item", stuff)
        return self.loadIconFile(item.icon.iconFile if item.icon else "")

    def loadIconFile(self, iconFile):
        if iconFile:
            return self.fittingView.imageList.GetImageIndex(iconFile, "icons")
        else:
            return -1

BaseIcon.register()
