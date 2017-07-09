import csv

# noinspection PyPackageRequirements
import wx
from logbook import Logger

try:
    # noinspection PyPackageRequirements
    import wx.propgrid as wxpg
except:
    if wx.VERSION < (2, 9):
        raise ImportError("wx.propgrid is only available in wxPython >= 2.9")
    else:
        raise

from eos.db.gamedata.queries import getItem, getAttributeInfo
from service.market import Market
import gui.display as d
import gui.globalEvents as GE
import gui.builtinMarketBrowser.pfSearchBox as SBox
from gui.marketBrowser import SearchBox
from gui.bitmapLoader import BitmapLoader

pyfalog = Logger(__name__)


class AttributeEditor(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Attribute Editor", pos=wx.DefaultPosition,
                          size=wx.Size(650, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileImport = fileMenu.Append(wx.ID_ANY, 'Import', 'Import overrides')
        fileExport = fileMenu.Append(wx.ID_ANY, 'Export', 'Import overrides')
        fileClear = fileMenu.Append(wx.ID_ANY, 'Clear All', 'Clear all overrides')

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnImport, fileImport)
        self.Bind(wx.EVT_MENU, self.OnExport, fileExport)
        self.Bind(wx.EVT_MENU, self.OnClear, fileClear)

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent
        self.panel = panel = wx.Panel(self, wx.ID_ANY)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftPanel = wx.Panel(panel, wx.ID_ANY,
                             style=wx.DOUBLE_BORDER if 'wxMSW' in wx.PlatformInfo else wx.SIMPLE_BORDER)

        self.searchBox = SearchBox(leftPanel)
        self.itemView = ItemView(leftPanel)

        leftSizer.Add(self.searchBox, 0, wx.EXPAND)
        leftSizer.Add(self.itemView, 1, wx.EXPAND)

        leftPanel.SetSizer(leftSizer)
        mainSizer.Add(leftPanel, 1, wx.ALL | wx.EXPAND, 5)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.btnRemoveOverrides = wx.Button(panel, wx.ID_ANY, u"Remove Overides for Item", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.pg = AttributeGrid(panel)
        rightSizer.Add(self.pg, 1, wx.ALL | wx.EXPAND, 5)
        rightSizer.Add(self.btnRemoveOverrides, 0, wx.ALL | wx.EXPAND, 5)
        self.btnRemoveOverrides.Bind(wx.EVT_BUTTON, self.pg.removeOverrides)
        self.btnRemoveOverrides.Enable(False)

        mainSizer.Add(rightSizer, 1, wx.EXPAND)

        panel.SetSizer(mainSizer)
        mainSizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        self.Destroy()

    def OnImport(self, event):
        dlg = wx.FileDialog(self, "Import pyfa override file",
                            wildcard="pyfa override file (*.csv)|*.csv",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'rb') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    itemID, attrID, value = row
                    item = getItem(int(itemID))
                    attr = getAttributeInfo(int(attrID))
                    item.setOverride(attr, float(value))
            self.itemView.updateItems(True)

    def OnExport(self, event):
        sMkt = Market.getInstance()
        items = sMkt.getItemsWithOverrides()
        defaultFile = "pyfa_overrides.csv"

        dlg = wx.FileDialog(self, "Save Overrides As...",
                            wildcard="pyfa overrides (*.csv)|*.csv",
                            style=wx.FD_SAVE,
                            defaultFile=defaultFile)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, 'wb') as csvfile:
                writer = csv.writer(csvfile)
                for item in items:
                    for key, override in item.overrides.iteritems():
                        writer.writerow([item.ID, override.attrID, override.value])

    def OnClear(self, event):
        dlg = wx.MessageDialog(
            self,
            "Are you sure you want to delete all overrides?",
            "Confirm Delete",
            wx.YES | wx.NO | wx.ICON_EXCLAMATION
        )

        if dlg.ShowModal() == wx.ID_YES:
            sMkt = Market.getInstance()
            items = sMkt.getItemsWithOverrides()
            # We can't just delete overrides, as loaded items will still have
            # them assigned. Deleting them from the database won't propagate
            # them due to the eve/user database disconnect. We must loop through
            # all items that have overrides and remove them
            for item in items:
                for _, x in item.overrides.items():
                    item.deleteOverride(x.attr)
            self.itemView.updateItems(True)
            self.pg.Clear()


# This is literally a stripped down version of the market.
class ItemView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        sMkt = Market.getInstance()

        self.things = sMkt.getItemsWithOverrides()
        self.items = self.things

        self.searchBox = parent.Parent.Parent.searchBox
        # Bind search actions
        self.searchBox.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        self.searchBox.Bind(SBox.EVT_TEXT, self.scheduleSearch)

        self.update(self.items)

    def clearSearch(self, event=None):
        if event:
            self.searchBox.Clear()
        self.items = self.things
        self.update(self.items)

    def updateItems(self, updateDisplay=False):
        sMkt = Market.getInstance()
        self.things = sMkt.getItemsWithOverrides()
        self.items = self.things
        if updateDisplay:
            self.update(self.things)

    def scheduleSearch(self, event=None):
        sMkt = Market.getInstance()

        search = self.searchBox.GetLineText(0)
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        # Show nothing if query is too short
        if len(realsearch) < 3:
            self.clearSearch()
            return

        sMkt.searchItems(search, self.populateSearch, False)

    def populateSearch(self, items):
        self.items = list(items)
        self.update(items)


class AttributeGrid(wxpg.PropertyGrid):
    def __init__(self, parent):
        wxpg.PropertyGrid.__init__(self, parent,
                                   style=wxpg.PG_HIDE_MARGIN | wxpg.PG_HIDE_CATEGORIES | wxpg.PG_BOLD_MODIFIED | wxpg.PG_TOOLTIPS)
        self.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        self.item = None

        self.itemView = parent.Parent.itemView

        self.btn = parent.Parent.btnRemoveOverrides

        self.Bind(wxpg.EVT_PG_CHANGED, self.OnPropGridChange)
        self.Bind(wxpg.EVT_PG_SELECTED, self.OnPropGridSelect)
        self.Bind(wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick)

        self.itemView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.itemActivated)
        self.itemView.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)

    def itemActivated(self, event):
        self.Clear()
        self.btn.Enable(True)
        sel = event.EventObject.GetFirstSelected()
        self.item = item = self.itemView.items[sel]

        for key in sorted(item.attributes.keys()):
            override = item.overrides.get(key, None)
            default = item.attributes[key].value
            if override and override.value != default:
                prop = wxpg.FloatProperty(key, value=override.value)
                prop.SetModifiedStatus(True)
            else:
                prop = wxpg.FloatProperty(key, value=default)

            prop.SetClientData(item.attributes[key])  # set this so that we may access it later
            prop.SetHelpString("%s\n%s" % (item.attributes[key].displayName or key, "Default Value: %0.3f" % default))
            self.Append(prop)

    def removeOverrides(self, event):
        if self.item is None:
            return

        for x in self.item.overrides.values():
            self.item.deleteOverride(x.attr)
            self.itemView.updateItems(True)
        self.ClearModifiedStatus()
        self.itemView.Select(self.itemView.GetFirstSelected(), on=False)
        self.Clear()

    def Clear(self):
        self.item = None
        self.btn.Enable(False)
        wxpg.PropertyGrid.Clear(self)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        attr = p.GetClientData()
        if p.GetValue() == attr.value:
            self.item.deleteOverride(attr)
            p.SetModifiedStatus(False)
        else:
            self.item.setOverride(attr, p.GetValue())

        self.itemView.updateItems()

        pyfalog.debug('{0} changed to "{1}"', p.GetName(), p.GetValueAsString())

    def OnPropGridSelect(self, event):
        pass

    def OnPropGridRightClick(self, event):
        pass
