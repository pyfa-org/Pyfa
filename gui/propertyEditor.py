import wx
import wx.propgrid as wxpg
import eos.db

import gui.PFSearchBox as SBox
from gui.marketBrowser import SearchBox
import gui.display as d
import service

import logging

logger = logging.getLogger(__name__)

class AttributeEditor( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Attribute Editor", size=wx.Size(700,500))

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)

        self.searchBox = SearchBox(panel, style=wx.DOUBLE_BORDER if 'wxMSW' in wx.PlatformInfo else wx.SIMPLE_BORDER)
        self.itemView = ItemView(panel)
        self.pg = AttributeGrid(panel)

        topsizer.Add(leftsizer, 1, wx.ALL|wx.EXPAND, 5)
        topsizer.Add(self.pg, 1, wx.ALL|wx.EXPAND, 5)

        leftsizer.Add(self.searchBox, 0, wx.EXPAND)
        leftsizer.Add(self.itemView, 1, wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


# This is literally a stripped down version of the market.
class ItemView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:power,,,True",
                    "attr:cpu,,,True"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.parent = parent
        sMkt = service.Market.getInstance()
        self.things = sMkt.getItemsWithOverrides()
        self.items = self.things

        # Bind search actions
        parent.Parent.searchBox.Bind(SBox.EVT_TEXT_ENTER, self.scheduleSearch)
        parent.Parent.searchBox.Bind(SBox.EVT_SEARCH_BTN, self.scheduleSearch)
        parent.Parent.searchBox.Bind(SBox.EVT_CANCEL_BTN, self.clearSearch)
        parent.Parent.searchBox.Bind(SBox.EVT_TEXT, self.scheduleSearch)

        self.update(self.items)

    def clearSearch(self, event=None):
        if event:
            self.parent.Parent.searchBox.Clear()
        self.items = self.things
        self.update(self.items)

    def scheduleSearch(self, event=None):
        sMkt = service.Market.getInstance()

        search = self.parent.Parent.searchBox.GetLineText(0)
        # Make sure we do not count wildcard as search symbol
        realsearch = search.replace("*", "")
        # Show nothing if query is too short
        if len(realsearch) < 3:
            self.clearSearch()
            return

        self.parent.searchMode = True
        sMkt.searchItems(search, self.populateSearch, False)

    def populateSearch(self, items):
        self.items = list(items)
        self.update(items)


class AttributeGrid(wxpg.PropertyGrid):

    def __init__(self, parent):
        wxpg.PropertyGrid.__init__(self, parent, style=wxpg.PG_HIDE_MARGIN|wxpg.PG_HIDE_CATEGORIES|wxpg.PG_BOLD_MODIFIED|wxpg.PG_TOOLTIPS)
        self.parent = parent

        self.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        self.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        self.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        parent.Parent.itemView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.itemActivated)
        parent.Parent.itemView.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.itemActivated)

    def itemActivated(self, event):
        self.Clear()
        sel = event.EventObject.GetFirstSelected()
        item = self.parent.Parent.itemView.items[sel]

        for key in sorted(item.attributes.keys()):
            override = item.overrides.get(key, None)
            default = item.attributes[key].value
            if override and override != item.attributes[key].value:
                prop = wxpg.FloatProperty(key, value=override)
                prop.defaultValue = default
                prop.SetModifiedStatus(True)
            else:
                prop = wxpg.FloatProperty(key, value=default)

            self.Append(prop)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            logger.debug('%s changed to "%s"' % (p.GetName(), p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            logger.debug('%s selected' % (event.GetProperty().GetName()))
        else:
            logger.debug('Nothing selected')

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            logger.debug('%s right clicked' % (event.GetProperty().GetName()))
        else:
            logger.debug('Nothing right clicked')
