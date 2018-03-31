# noinspection PyPackageRequirements
import wx

from .helpers import AutoListCtrl
from service.price import Price as ServicePrice
from service.market import Market
from service.attribute import Attribute
from gui.utils.numberFormatter import formatAmount


class ItemCompare(wx.Panel):
    def __init__(self, parent, stuff, item, items, context=None):
        # Start dealing with Price stuff to get that thread going
        sPrice = ServicePrice.getInstance()
        sPrice.getPrices(items, self.UpdateList)

        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.paramList = AutoListCtrl(self, wx.ID_ANY,
                                      style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.NO_BORDER)
        mainSizer.Add(self.paramList, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self.toggleView = 1
        self.stuff = stuff
        self.currentSort = None
        self.sortReverse = False
        self.item = item
        self.items = sorted(items,
                            key=lambda x: x.attributes['metaLevel'].value if 'metaLevel' in x.attributes else 0)
        self.attrs = {}

        # get a dict of attrName: attrInfo of all unique attributes across all items
        for item in self.items:
            for attr in list(item.attributes.keys()):
                if item.attributes[attr].info.displayName:
                    self.attrs[attr] = item.attributes[attr].info

        # Process attributes for items and find ones that differ
        for attr in list(self.attrs.keys()):
            value = None

            for item in self.items:
                # we can automatically break here if this item doesn't have the attribute,
                # as that means at least one item did
                if attr not in item.attributes:
                    break

                # this is the first attribute for the item set, set the initial value
                if value is None:
                    value = item.attributes[attr].value
                    continue

                if attr not in item.attributes or item.attributes[attr].value != value:
                    break
            else:
                # attribute values were all the same, delete
                del self.attrs[attr]

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.totalAttrsLabel = wx.StaticText(self, wx.ID_ANY, " ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, "Toggle view mode", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.refreshBtn = wx.Button(self, wx.ID_ANY, "Refresh", wx.DefaultPosition, wx.DefaultSize,
                                    wx.BU_EXACTFIT)
        bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.RefreshValues)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)

        self.PopulateList()

        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleViewMode)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.SortCompareCols)

    def SortCompareCols(self, event):
        self.Freeze()
        self.paramList.ClearAll()
        self.PopulateList(event.Column)
        self.Thaw()

    def UpdateList(self, items=None):
        # We do nothing with `items`, but it gets returned by the price service thread
        self.Freeze()
        self.paramList.ClearAll()
        self.PopulateList()
        self.Thaw()
        self.paramList.resizeLastColumn(100)

    def RefreshValues(self, event):
        self.UpdateList()
        event.Skip()

    def ToggleViewMode(self, event):
        self.toggleView *= -1
        self.UpdateList()
        event.Skip()

    def processPrices(self, prices):
        for i, price in enumerate(prices):
            self.paramList.SetItem(i, len(self.attrs) + 1, formatAmount(price.value, 3, 3, 9, currency=True))

    def PopulateList(self, sort=None):

        if sort is not None and self.currentSort == sort:
            self.sortReverse = not self.sortReverse
        else:
            self.currentSort = sort
            self.sortReverse = False

        if sort is not None:
            if sort == 0:  # Name sort
                func = lambda _val: _val.name
            else:
                try:
                    # Remember to reduce by 1, because the attrs array
                    # starts at 0 while the list has the item name as column 0.
                    attr = str(list(self.attrs.keys())[sort - 1])
                    func = lambda _val: _val.attributes[attr].value if attr in _val.attributes else None
                except IndexError:
                    # Clicked on a column that's not part of our array (price most likely)
                    self.sortReverse = False
                    func = lambda _val: _val.attributes['metaLevel'].value if 'metaLevel' in _val.attributes else None

            self.items = sorted(self.items, key=func, reverse=self.sortReverse)

        self.paramList.InsertColumn(0, "Item")
        self.paramList.SetColumnWidth(0, 200)

        for i, attr in enumerate(self.attrs.keys()):
            name = self.attrs[attr].displayName if self.attrs[attr].displayName else attr
            self.paramList.InsertColumn(i + 1, name)
            self.paramList.SetColumnWidth(i + 1, 120)

        self.paramList.InsertColumn(len(self.attrs) + 1, "Price")
        self.paramList.SetColumnWidth(len(self.attrs) + 1, 60)

        for item in self.items:
            i = self.paramList.InsertItem(self.paramList.GetItemCount(), item.name)
            for x, attr in enumerate(self.attrs.keys()):
                if attr in item.attributes:
                    info = self.attrs[attr]
                    value = item.attributes[attr].value
                    if self.toggleView != 1:
                        valueUnit = str(value)
                    elif info and info.unit and self.toggleView == 1:
                        valueUnit = self.TranslateValueUnit(value, info.unit.displayName, info.unit.name)
                    else:
                        valueUnit = formatAmount(value, 3, 0, 0)

                    self.paramList.SetItem(i, x + 1, valueUnit)

            # Add prices
            self.paramList.SetItem(i, len(self.attrs) + 1, formatAmount(item.price.price, 3, 3, 9, currency=True))

        self.paramList.RefreshRows()
        self.Layout()

    @staticmethod
    def TranslateValueUnit(value, unitName, unitDisplayName):
        def itemIDCallback():
            item = Market.getInstance().getItem(value)
            return "%s (%d)" % (item.name, value) if item is not None else str(value)

        def groupIDCallback():
            group = Market.getInstance().getGroup(value)
            return "%s (%d)" % (group.name, value) if group is not None else str(value)

        def attributeIDCallback():
            attribute = Attribute.getInstance().getAttributeInfo(value)
            return "%s (%d)" % (attribute.name.capitalize(), value)

        trans = {
            "Inverse Absolute Percent" : (lambda: (1 - value) * 100, unitName),
            "Inversed Modifier Percent": (lambda: (1 - value) * 100, unitName),
            "Modifier Percent"         : (lambda: ("%+.2f" if ((value - 1) * 100) % 1 else "%+d") % ((value - 1) * 100), unitName),
            "Volume"                   : (lambda: value, "m\u00B3"),
            "Sizeclass"                : (lambda: value, ""),
            "Absolute Percent"         : (lambda: (value * 100), unitName),
            "Milliseconds"             : (lambda: value / 1000.0, unitName),
            "typeID"                   : (itemIDCallback, ""),
            "groupID"                  : (groupIDCallback, ""),
            "attributeID"              : (attributeIDCallback, "")
        }

        override = trans.get(unitDisplayName)
        if override is not None:
            v = override[0]()
            if isinstance(v, str):
                fvalue = v
            elif isinstance(v, (int, float)):
                fvalue = formatAmount(v, 3, 0, 0)
            else:
                fvalue = v
            return "%s %s" % (fvalue, override[1])
        else:
            return "%s %s" % (formatAmount(value, 3, 0), unitName)
