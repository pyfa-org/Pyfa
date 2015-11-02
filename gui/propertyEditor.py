import wx
import wx.propgrid as wxpg

import gui.PFSearchBox as SBox
from gui.marketBrowser import SearchBox
import gui.display as d
import gui.globalEvents as GE
from gui.bitmapLoader import BitmapLoader
import service

import logging

logger = logging.getLogger(__name__)

class AttributeEditor( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Attribute Editor", pos=wx.DefaultPosition,
                            size=wx.Size(650, 600), style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT|wx.TAB_TRAVERSAL)

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
        self.SetIcon(i)

        self.mainFrame = parent
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)

        leftsizer = wx.BoxSizer(wx.VERTICAL)
        leftPanel = wx.Panel(panel, wx.ID_ANY, style=wx.DOUBLE_BORDER if 'wxMSW' in wx.PlatformInfo else wx.SIMPLE_BORDER)

        self.searchBox = SearchBox(leftPanel)
        self.itemView = ItemView(leftPanel)

        leftsizer.Add(self.searchBox, 0, wx.EXPAND)
        leftsizer.Add(self.itemView, 1, wx.EXPAND)

        leftPanel.SetSizer(leftsizer)
        topsizer.Add(leftPanel, 1, wx.ALL | wx.EXPAND, 5)

        self.pg = AttributeGrid(panel)
        topsizer.Add(self.pg, 1, wx.ALL|wx.EXPAND, 5)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

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


# This is literally a stripped down version of the market.
class ItemView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        sMkt = service.Market.getInstance()

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

    def updateItems(self):
        sMkt = service.Market.getInstance()
        self.things = sMkt.getItemsWithOverrides()

    def scheduleSearch(self, event=None):
        sMkt = service.Market.getInstance()

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
        wxpg.PropertyGrid.__init__(self, parent, style=wxpg.PG_HIDE_MARGIN|wxpg.PG_HIDE_CATEGORIES|wxpg.PG_BOLD_MODIFIED|wxpg.PG_TOOLTIPS)
        self.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        self.item = None

        self.itemView = parent.Parent.itemView

        self.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        self.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        self.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        self.itemView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.itemActivated)
        self.itemView.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)

    def itemActivated(self, event):
        self.Clear()
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
            prop.SetHelpString("%s\n%s"%(item.attributes[key].displayName or key, "Default Value: %0.2f"%default))
            self.Append(prop)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        attr = p.GetClientData()
        if p.GetValue() == attr.value:
            self.item.deleteOverride(attr)
            p.SetModifiedStatus(False)
        else:
            self.item.setOverride(attr, p.GetValue())

        self.itemView.updateItems()

        logger.debug('%s changed to "%s"' % (p.GetName(), p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        pass

    def OnPropGridRightClick(self, event):
        pass
