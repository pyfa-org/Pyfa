import wx
import service
import bitmapLoader
import gui.mainFrame
import  wx.lib.newevent
import sys

FitCreated, EVT_FIT_CREATED = wx.lib.newevent.NewEvent()
FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.built = False
        self.viewSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.viewSizer)

        self.shipMenu = ShipMenu(self)
        self.viewSizer.Add(self.shipMenu, 0, wx.EXPAND)

        self.shipView = ShipView(self)
        self.viewSizer.Add(self.shipView, 1, wx.EXPAND)

    def getSelectedFitID(self):
        tree = self.getActiveTree()
        selection = tree.GetSelection()
        if selection.IsOk():
            data = tree.GetPyData(selection)
            if data is not None:
                type, fitID = data
                if type == "fit":
                    return fitID


class ShipView(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_ICON | wx.LC_AUTOARRANGE | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS)
        self.rename = False

        self.shipImageList = wx.ImageList(24, 24)
        self.SetImageList(self.shipImageList, wx.IMAGE_LIST_NORMAL)

        cMarket = service.Market.getInstance()
        shipRoot = cMarket.getShipRoot()
        shipRoot.sort(key=lambda i: i[1])
        iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_big", "icons"))
        for id, name in shipRoot:
            index = self.InsertImageStringItem(sys.maxint, name, iconId)
            self.SetItemData(index, id)

class ShipMenu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        size = None
        for name, art in (("new", wx.ART_NEW), ("rename", bitmapLoader.getBitmap("rename", "icons")), ("copy", wx.ART_COPY), ("delete", wx.ART_DELETE)):
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
            if size is None:
                size = btn.GetSize()

            btn.SetMinSize(size)
            btn.SetMaxSize(size)

            btn.Layout()
            setattr(self, name, btn)
            btn.Enable(False)
            btn.SetToolTipString("%s fit" % name.capitalize())
            sizer.Add(btn, 0, wx.EXPAND)

        p = wx.Panel(self)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(psizer)

        self.search = wx.SearchCtrl(p, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        psizer.Add(self.search, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#        p.SetMinSize((wx.SIZE_AUTO_WIDTH, 27))
        sizer.Add(p, 1, wx.EXPAND)

