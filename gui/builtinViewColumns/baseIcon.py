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
        self.mask = wx.LIST_MASK_TEXT
        self.columnText = ""
        self.shipImage = fittingView.imageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))

    def getImageId(self, stuff):
        if isinstance(stuff, Drone):
            return -1
        if isinstance(stuff, Fit):
            return self.shipImage
        if isinstance(stuff, Module):
            if stuff.isEmpty:
                bitmap = bitmapLoader.getBitmap("slot_%s_small" % Slot.getName(stuff.slot).lower(), "icons")
                return self.fittingView.imageList.Add(bitmap)
            else:
                return self.loadIconFile(stuff.item.icon.iconFile if stuff.item.icon else "")

        item = getattr(stuff, "item", stuff)
        return self.loadIconFile(item.icon.iconFile if item.icon else "")

    def loadIconFile(self, iconFile):
        if iconFile:
            bitmap = bitmapLoader.getBitmap(iconFile, "pack")
            if bitmap is None:
                return -1
            else:
                return self.fittingView.imageList.Add(bitmap)
        else:
            return -1

BaseIcon.register()
