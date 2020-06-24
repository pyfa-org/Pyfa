import csv

# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import wx.propgrid as wxpg
from logbook import Logger

import gui.builtinMarketBrowser.pfSearchBox as SBox
import gui.display as d
import gui.globalEvents as GE
from eos.db.gamedata.queries import getAttributeInfo, getItem
from gui.auxWindow import AuxiliaryFrame
from gui.bitmap_loader import BitmapLoader
from gui.marketBrowser import SearchBox
from service.fit import Fit
from service.market import Market

pyfalog = Logger(__name__)

_t = wx.GetTranslation


class AttributeEditor(AuxiliaryFrame):

    def __init__(self, parent):
        super().__init__(
                parent, wx.ID_ANY, title=_t("Attribute Editor"), pos=wx.DefaultPosition,
                size=wx.Size(650, 600), resizeable=True)

        i = wx.Icon(BitmapLoader.getBitmap("fit_rename_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileImport = fileMenu.Append(wx.ID_ANY, _t('Import'), _t('Import overrides'))
        fileExport = fileMenu.Append(wx.ID_ANY, _t('Export'), _t('Import overrides'))
        fileClear = fileMenu.Append(wx.ID_ANY, _t('Clear All'), _t('Clear all overrides'))

        menubar.Append(fileMenu, _t('&File'))
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnImport, fileImport)
        self.Bind(wx.EVT_MENU, self.OnExport, fileExport)
        self.Bind(wx.EVT_MENU, self.OnClear, fileClear)

        i = wx.Icon(BitmapLoader.getBitmap("fit_rename_small", "gui"))
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
        self.btnRemoveOverrides = wx.Button(panel, wx.ID_ANY, _t("Remove Overides for Item"), wx.DefaultPosition,
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
        self.SetMinSize(self.GetSize())

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()

    def OnClose(self, event):
        fitID = self.mainFrame.getActiveFit()
        if fitID is not None:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitIDs=(fitID,)))
        event.Skip()

    def OnImport(self, event):
        with wx.FileDialog(
                self, _t("Import pyfa override file"),
                wildcard=_t("pyfa override file") + " (*.csv)|*.csv",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                with open(path, 'r') as csvfile:
                    spamreader = csv.reader(csvfile)
                    for row in spamreader:
                        if len(row) == 0:  # csvwriter seems to added blank lines to the end sometimes
                            continue
                        itemID, attrID, value = row
                        item = getItem(int(itemID))
                        attr = getAttributeInfo(int(attrID))
                        item.setOverride(attr, float(value))
                self.itemView.updateItems(True)

    def OnExport(self, event):
        sMkt = Market.getInstance()
        items = sMkt.getItemsWithOverrides()
        defaultFile = "pyfa_overrides.csv"

        with wx.FileDialog(
                self, _t("Save Overrides As..."),
                wildcard=_t("pyfa overrides") + " (*.csv)|*.csv",
                style=wx.FD_SAVE,
                defaultFile=defaultFile
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                with open(path, 'w', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for item in items:
                        for key, override in item.overrides.items():
                            writer.writerow([item.ID, override.attrID, override.value])

    def OnClear(self, event):
        with wx.MessageDialog(
                self,
                _t("Are you sure you want to delete all overrides?"),
                _t("Confirm Delete"),
                wx.YES | wx.NO | wx.ICON_EXCLAMATION
        ) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                sMkt = Market.getInstance()
                items = sMkt.getItemsWithOverrides()
                # We can't just delete overrides, as loaded items will still have
                # them assigned. Deleting them from the database won't propagate
                # them due to the eve/user database disconnect. We must loop through
                # all items that have overrides and remove them
                for item in items:
                    for _, x in list(item.overrides.items()):
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
        self.activeItems = []

        self.searchTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.scheduleSearch, self.searchTimer)

        self.searchBox = parent.Parent.Parent.searchBox
        # Bind search actions
        self.searchBox.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        self.searchBox.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        self.searchBox.Bind(SBox.EVT_TEXT, self.delaySearch)

        self.update(Market.getInstance().getItemsWithOverrides())

    def clearSearch(self, event=None):
        if event:
            self.searchBox.Clear()
        self.update(Market.getInstance().getItemsWithOverrides())

    def updateItems(self, updateDisplay=False):
        if updateDisplay:
            self.update(Market.getInstance().getItemsWithOverrides())

    def delaySearch(self, evt):
        sFit = Fit.getInstance()
        self.searchTimer.Stop()
        self.searchTimer.Start(sFit.serviceFittingOptions["marketSearchDelay"], True)

    def scheduleSearch(self, event=None):
        sMkt = Market.getInstance()

        search = self.searchBox.GetLineText(0)
        # Make sure we do not count wildcards as search symbol
        realsearch = search.replace('*', '').replace('?', '')
        # Show nothing if query is too short
        if len(realsearch) < 3:
            self.clearSearch()
            return

        sMkt.searchItems(search, self.populateSearch, 'everything')

    def itemSort(self, item):
        sMkt = Market.getInstance()
        isFittable = item.group.name in sMkt.FIT_GROUPS or item.category.name in sMkt.FIT_CATEGORIES
        return (not isFittable, *sMkt.itemSort(item))

    def populateSearch(self, itemIDs):
        items = Market.getItems(itemIDs)
        self.update(items)

    def populate(self, items):
        if len(items) > 0:
            self.unselectAll()
            items.sort(key=self.itemSort)
        self.activeItems = items
        d.Display.populate(self, items)

    def refresh(self, items):
        if len(items) > 1:
            items.sort(key=self.itemSort)
        d.Display.refresh(self, items)


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
        self.item = item = self.itemView.activeItems[sel]

        for key in sorted(item.attributes.keys()):
            override = item.overrides.get(key, None)
            default = item.attributes[key].value
            if override and override.value != default:
                prop = wxpg.FloatProperty(key, value=override.value)
                prop.SetModifiedStatus(True)
            else:
                prop = wxpg.FloatProperty(key, value=default)

            prop.SetClientData(item.attributes[key])  # set this so that we may access it later
            prop.SetHelpString("%s\n%s" % (item.attributes[key].displayName or key, _t("Default Value: %0.3f") % default))
            self.Append(prop)

    def removeOverrides(self, event):
        if self.item is None:
            return

        for x in list(self.item.overrides.values()):
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
