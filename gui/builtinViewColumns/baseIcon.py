from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
from gui import bitmapLoader
import wx
from eos.types import Drone, Fit, Module, Slot

class BaseIcon(ViewColumn):
    name = "Base Icon"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.size = 16
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_IMAGE
        self.columnText = ""
        self.shipImage = fittingView.imageList.GetImageIndex("ship_small", "icons")

    def getImageId(self, stuff):
        if isinstance(stuff, Drone):
            return -1
        if isinstance(stuff, Fit):
            return self.shipImage
        if isinstance(stuff, Module):
            if stuff.isEmpty:
                return self.fittingView.imageList.GetImageIndex("slot_%s_small" % Slot.getName(stuff.slot).lower(), "icons")
            else:
                return self.loadIconFile(stuff.item.icon.iconFile if stuff.item.icon else "")

        item = getattr(stuff, "item", stuff)
        return self.loadIconFile(item.icon.iconFile if item.icon else "")

    def loadIconFile(self, iconFile):
        if iconFile:
            return self.fittingView.imageList.GetImageIndex(iconFile, "pack")
        else:
            return -1

BaseIcon.register()
