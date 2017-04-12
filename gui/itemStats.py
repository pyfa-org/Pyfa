# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import re
import os
import csv
import sys
import subprocess

# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import wx.html
# noinspection PyPackageRequirements
import wx.lib.mixins.listctrl as listmix

import config
from eos.saveddata.mode import Mode
from eos.saveddata.character import Skill
from eos.saveddata.implant import Implant
from eos.saveddata.booster import Booster
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from eos.saveddata.citadel import Citadel
from eos.saveddata.fit import Fit
from service.market import Market
from service.attribute import Attribute
from service.price import Price as ServicePrice
import gui.mainFrame
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.contextMenu import ContextMenu


class ItemStatsDialog(wx.Dialog):
    counter = 0

    def __init__(
            self,
            victim,
            fullContext=None,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            maximized=False
    ):

        wx.Dialog.__init__(
                self,
                gui.mainFrame.MainFrame.getInstance(),
                wx.ID_ANY,
                title="Item stats",
                pos=pos,
                size=size,
                style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU
        )

        empty = getattr(victim, "isEmpty", False)

        if empty:
            self.Hide()
            self.Destroy()
            return

        srcContext = fullContext[0]
        try:
            itmContext = fullContext[1]
        except IndexError:
            itmContext = None
        item = getattr(victim, "item", None) if srcContext.lower() not in (
            "projectedcharge",
            "fittingcharge"
        ) else getattr(victim, "charge", None)
        if item is None:
            sMkt = Market.getInstance()
            item = sMkt.getItem(victim.ID)
            victim = None
        self.context = itmContext
        if item.icon is not None:
            before, sep, after = item.icon.iconFile.rpartition("_")
            iconFile = "%s%s%s" % (before, sep, "0%s" % after if len(after) < 2 else after)
            itemImg = BitmapLoader.getBitmap(iconFile, "icons")
            if itemImg is not None:
                self.SetIcon(wx.IconFromBitmap(itemImg))
        self.SetTitle("%s: %s%s" % ("%s Stats" % itmContext if itmContext is not None else "Stats", item.name,
                                    " (%d)" % item.ID if config.debug else ""))

        self.SetMinSize((300, 200))
        if "wxGTK" in wx.PlatformInfo:  # GTK has huge tab widgets, give it a bit more room
            self.SetSize((580, 500))
        else:
            self.SetSize((550, 500))
        # self.SetMaxSize((500, -1))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.container = ItemStatsContainer(self, victim, item, itmContext)
        self.mainSizer.Add(self.container, 1, wx.EXPAND)

        if "wxGTK" in wx.PlatformInfo:
            self.closeBtn = wx.Button(self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0)
            self.mainSizer.Add(self.closeBtn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
            self.closeBtn.Bind(wx.EVT_BUTTON, self.closeEvent)

        self.SetSizer(self.mainSizer)

        self.parentWnd = gui.mainFrame.MainFrame.getInstance()

        dlgsize = self.GetSize()
        psize = self.parentWnd.GetSize()
        ppos = self.parentWnd.GetPosition()

        ItemStatsDialog.counter += 1
        self.dlgOrder = ItemStatsDialog.counter

        counter = ItemStatsDialog.counter
        dlgStep = 30
        if counter * dlgStep > ppos.x + psize.width - dlgsize.x or counter * dlgStep > ppos.y + psize.height - dlgsize.y:
            ItemStatsDialog.counter = 1

        dlgx = ppos.x + counter * dlgStep
        dlgy = ppos.y + counter * dlgStep
        if pos == wx.DefaultPosition:
            self.SetPosition((dlgx, dlgy))
        else:
            self.SetPosition(pos)
        if maximized:
            self.Maximize(True)
        else:
            if size != wx.DefaultSize:
                self.SetSize(size)
        self.parentWnd.RegisterStatsWindow(self)

        self.Show()

        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)

    def OnActivate(self, event):
        self.parentWnd.SetActiveStatsWindow(self)

    def closeEvent(self, event):

        if self.dlgOrder == ItemStatsDialog.counter:
            ItemStatsDialog.counter -= 1
        self.parentWnd.UnregisterStatsWindow(self)

        self.Destroy()


class ItemStatsContainer(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        sMkt = Market.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.nbContainer = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        mainSizer.Add(self.nbContainer, 1, wx.EXPAND | wx.ALL, 2)

        if item.traits is not None:
            self.traits = ItemTraits(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.traits, "Traits")

        self.desc = ItemDescription(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.desc, "Description")

        self.params = ItemParams(self.nbContainer, stuff, item, context)
        self.nbContainer.AddPage(self.params, "Attributes")

        items = sMkt.getVariationsByItems([item])
        if len(items) > 1:
            self.compare = ItemCompare(self.nbContainer, stuff, item, items, context)
            self.nbContainer.AddPage(self.compare, "Compare")

        self.reqs = ItemRequirements(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.reqs, "Requirements")

        self.effects = ItemEffects(self.nbContainer, stuff, item)
        self.nbContainer.AddPage(self.effects, "Effects")

        if stuff is not None:
            self.affectedby = ItemAffectedBy(self.nbContainer, stuff, item)
            self.nbContainer.AddPage(self.affectedby, "Affected by")

        if config.debug:
            self.properties = ItemProperties(self.nbContainer, stuff, item, context)
            self.nbContainer.AddPage(self.properties, "Properties")

        self.nbContainer.Bind(wx.EVT_LEFT_DOWN, self.mouseHit)
        self.SetSizer(mainSizer)
        self.Layout()

    def __del__(self):
        pass

    def mouseHit(self, event):
        tab, _ = self.nbContainer.HitTest(event.Position)
        if tab != -1:
            self.nbContainer.SetSelection(tab)


class AutoListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)


class AutoListCtrlNoHighlight(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class ItemTraits(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        self.traits = wx.html.HtmlWindow(self)
        self.traits.SetPage(item.traits.traitText)

        mainSizer.Add(self.traits, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()


class ItemDescription(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        bgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        fgcolor = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        self.description = wx.html.HtmlWindow(self)

        if not item.description:
            return

        desc = item.description.replace("\n", "<br>")
        # Strip font tags
        desc = re.sub("<( *)font( *)color( *)=(.*?)>(?P<inside>.*?)<( *)/( *)font( *)>", "\g<inside>", desc)
        # Strip URLs
        desc = re.sub("<( *)a(.*?)>(?P<inside>.*?)<( *)/( *)a( *)>", "\g<inside>", desc)
        desc = "<body bgcolor='" + bgcolor.GetAsString(wx.C2S_HTML_SYNTAX) + "' text='" + fgcolor.GetAsString(
                wx.C2S_HTML_SYNTAX) + "' >" + desc + "</body>"

        self.description.SetPage(desc)

        mainSizer.Add(self.description, 1, wx.ALL | wx.EXPAND, 0)
        self.Layout()


class ItemParams(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.paramList = AutoListCtrl(self, wx.ID_ANY,
                                      style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.NO_BORDER)
        mainSizer.Add(self.paramList, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self.toggleView = 1
        self.stuff = stuff
        self.item = item
        self.attrInfo = {}
        self.attrValues = {}
        self._fetchValues()

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.totalAttrsLabel = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, u"Toggle view mode", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.exportStatsBtn = wx.ToggleButton(self, wx.ID_ANY, u"Export Item Stats", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        bSizer.Add(self.exportStatsBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
            bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
            self.refreshBtn.Bind(wx.EVT_BUTTON, self.RefreshValues)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)

        self.PopulateList()

        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleViewMode)
        self.exportStatsBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ExportItemStats)

    def _fetchValues(self):
        if self.stuff is None:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.item.attributes)
            self.attrValues.update(self.item.attributes)
        elif self.stuff.item == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.item.attributes)
            self.attrValues.update(self.stuff.itemModifiedAttributes)
        elif self.stuff.charge == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.charge.attributes)
            self.attrValues.update(self.stuff.chargeModifiedAttributes)
        # When item for stats window no longer exists, don't change anything
        else:
            return

    def UpdateList(self):
        self.Freeze()
        self.paramList.ClearAll()
        self.PopulateList()
        self.Thaw()
        self.paramList.resizeLastColumn(100)

    def RefreshValues(self, event):
        self._fetchValues()
        self.UpdateList()
        event.Skip()

    def ToggleViewMode(self, event):
        self.toggleView *= -1
        self.UpdateList()
        event.Skip()

    def ExportItemStats(self, event):
        exportFileName = self.item.name + " (" + str(self.item.ID) + ").csv"

        saveFileDialog = wx.FileDialog(self, "Save CSV file", "", exportFileName,
                                       "CSV files (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # the user hit cancel...

        with open(saveFileDialog.GetPath(), "wb") as exportFile:
            writer = csv.writer(exportFile, delimiter=',')

            writer.writerow(
                    [
                        "ID",
                        "Internal Name",
                        "Friendly Name",
                        "Modified Value",
                        "Base Value",
                    ]
            )

            for attribute in self.attrValues:

                try:
                    attribute_id = self.attrInfo[attribute].ID
                except (KeyError, AttributeError):
                    attribute_id = ''

                try:
                    attribute_name = self.attrInfo[attribute].name
                except (KeyError, AttributeError):
                    attribute_name = attribute

                try:
                    attribute_displayname = self.attrInfo[attribute].displayName
                except (KeyError, AttributeError):
                    attribute_displayname = ''

                try:
                    attribute_value = self.attrInfo[attribute].value
                except (KeyError, AttributeError):
                    attribute_value = ''

                try:
                    attribute_modified_value = self.attrValues[attribute].value
                except (KeyError, AttributeError):
                    attribute_modified_value = self.attrValues[attribute]

                writer.writerow(
                        [
                            attribute_id,
                            attribute_name,
                            attribute_displayname,
                            attribute_modified_value,
                            attribute_value,
                        ]
                )

    def PopulateList(self):
        self.paramList.InsertColumn(0, "Attribute")
        self.paramList.InsertColumn(1, "Current Value")
        if self.stuff is not None:
            self.paramList.InsertColumn(2, "Base Value")
        self.paramList.SetColumnWidth(0, 110)
        self.paramList.SetColumnWidth(1, 90)
        if self.stuff is not None:
            self.paramList.SetColumnWidth(2, 90)
        self.paramList.setResizeColumn(0)
        self.imageList = wx.ImageList(16, 16)
        self.paramList.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)

        names = list(self.attrValues.iterkeys())
        names.sort()

        idNameMap = {}
        idCount = 0
        for name in names:
            info = self.attrInfo.get(name)
            att = self.attrValues[name]

            valDefault = getattr(info, "value", None)
            valueDefault = valDefault if valDefault is not None else att

            val = getattr(att, "value", None)
            value = val if val is not None else att

            if info and info.displayName and self.toggleView == 1:
                attrName = info.displayName
            else:
                attrName = name

            if info and config.debug:
                attrName += " ({})".format(info.ID)

            if info:
                if info.icon is not None:
                    iconFile = info.icon.iconFile
                    icon = BitmapLoader.getBitmap(iconFile, "icons")

                    if icon is None:
                        icon = BitmapLoader.getBitmap("transparent16x16", "gui")

                    attrIcon = self.imageList.Add(icon)
                else:
                    attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))
            else:
                attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))

            index = self.paramList.InsertImageStringItem(sys.maxint, attrName, attrIcon)
            idNameMap[idCount] = attrName
            self.paramList.SetItemData(index, idCount)
            idCount += 1

            if self.toggleView != 1:
                valueUnit = str(value)
            elif info and info.unit:
                valueUnit = self.TranslateValueUnit(value, info.unit.displayName, info.unit.name)
            else:
                valueUnit = formatAmount(value, 3, 0, 0)

            if self.toggleView != 1:
                valueUnitDefault = str(valueDefault)
            elif info and info.unit:
                valueUnitDefault = self.TranslateValueUnit(valueDefault, info.unit.displayName, info.unit.name)
            else:
                valueUnitDefault = formatAmount(valueDefault, 3, 0, 0)

            self.paramList.SetStringItem(index, 1, valueUnit)
            if self.stuff is not None:
                self.paramList.SetStringItem(index, 2, valueUnitDefault)

        self.paramList.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
        self.paramList.RefreshRows()
        self.totalAttrsLabel.SetLabel("%d attributes. " % idCount)
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
            "Modifier Percent"         : (
                lambda: ("%+.2f" if ((value - 1) * 100) % 1 else "%+d") % ((value - 1) * 100), unitName),
            "Volume"                   : (lambda: value, u"m\u00B3"),
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
            elif isinstance(v, (int, float, long)):
                fvalue = formatAmount(v, 3, 0, 0)
            else:
                fvalue = v
            return "%s %s" % (fvalue, override[1])
        else:
            return "%s %s" % (formatAmount(value, 3, 0), unitName)


class ItemCompare(wx.Panel):
    def __init__(self, parent, stuff, item, items, context=None):
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
                            key=lambda x: x.attributes['metaLevel'].value if 'metaLevel' in x.attributes else None)
        self.attrs = {}

        # get a dict of attrName: attrInfo of all unique attributes across all items
        for item in self.items:
            for attr in item.attributes.keys():
                if item.attributes[attr].info.displayName:
                    self.attrs[attr] = item.attributes[attr].info

        # Process attributes for items and find ones that differ
        for attr in self.attrs.keys():
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

        self.totalAttrsLabel = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, u"Toggle view mode", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize,
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

    def UpdateList(self):
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
            self.paramList.SetStringItem(i, len(self.attrs) + 1, formatAmount(price.value, 3, 3, 9, currency=True))

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
                    attr = str(self.attrs.keys()[sort - 1])
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
            i = self.paramList.InsertStringItem(sys.maxint, item.name)
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

                    self.paramList.SetStringItem(i, x + 1, valueUnit)

                # Add prices
                sPrice = ServicePrice.getInstance()
                self.paramList.SetStringItem(i, len(self.attrs) + 1, formatAmount(sPrice.getPriceNow(item), 3, 3, 9, currency=True))

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
            "Volume"                   : (lambda: value, u"m\u00B3"),
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
            elif isinstance(v, (int, float, long)):
                fvalue = formatAmount(v, 3, 0, 0)
            else:
                fvalue = v
            return "%s %s" % (fvalue, override[1])
        else:
            return "%s %s" % (formatAmount(value, 3, 0), unitName)


class ItemRequirements(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        # itemId is set by the parent.
        self.romanNb = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        self.skillIdHistory = []
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.reqTree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)

        mainSizer.Add(self.reqTree, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.root = self.reqTree.AddRoot("WINRARZOR")
        self.reqTree.SetPyData(self.root, None)

        self.imageList = wx.ImageList(16, 16)
        self.reqTree.SetImageList(self.imageList)
        skillBookId = self.imageList.Add(BitmapLoader.getBitmap("skill_small", "gui"))

        self.getFullSkillTree(item, self.root, skillBookId)

        self.reqTree.ExpandAll()

        self.Layout()

    def getFullSkillTree(self, parentSkill, parent, sbIconId):
        for skill, level in parentSkill.requiredSkills.iteritems():
            child = self.reqTree.AppendItem(parent, "%s  %s" % (skill.name, self.romanNb[int(level)]), sbIconId)
            if skill.ID not in self.skillIdHistory:
                self.getFullSkillTree(skill, child, sbIconId)
                self.skillIdHistory.append(skill.ID)


class ItemEffects(wx.Panel):
    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.item = item

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.effectList = AutoListCtrl(self, wx.ID_ANY,
                                       style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.NO_BORDER)
        mainSizer.Add(self.effectList, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick, self.effectList)
        if config.debug:
            self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick, self.effectList)

        self.PopulateList()

    def PopulateList(self):

        self.effectList.InsertColumn(0, "Name")
        self.effectList.InsertColumn(1, "Active")
        self.effectList.InsertColumn(2, "Type")
        if config.debug:
            self.effectList.InsertColumn(3, "Run Time")
            self.effectList.InsertColumn(4, "ID")

        # self.effectList.SetColumnWidth(0,385)

        self.effectList.setResizeColumn(0)
        self.effectList.SetColumnWidth(1, 50)
        self.effectList.SetColumnWidth(2, 80)
        if config.debug:
            self.effectList.SetColumnWidth(3, 65)
            self.effectList.SetColumnWidth(4, 40)

        item = self.item
        effects = item.effects
        names = list(effects.iterkeys())
        names.sort()

        for name in names:
            index = self.effectList.InsertStringItem(sys.maxint, name)

            if effects[name].isImplemented:
                if effects[name].activeByDefault:
                    activeByDefault = "Yes"
                else:
                    activeByDefault = "No"
            else:
                activeByDefault = ""

            effectTypeText = ""
            if effects[name].type:
                for effectType in effects[name].type:
                    effectTypeText += effectType + " "
                    pass

            if effects[name].runTime and effects[name].isImplemented:
                effectRunTime = str(effects[name].runTime)
            else:
                effectRunTime = ""

            self.effectList.SetStringItem(index, 1, activeByDefault)
            self.effectList.SetStringItem(index, 2, effectTypeText)
            if config.debug:
                self.effectList.SetStringItem(index, 3, effectRunTime)
                self.effectList.SetStringItem(index, 4, str(effects[name].ID))

        self.effectList.RefreshRows()
        self.Layout()

    def OnClick(self, event):
        """
        Debug use: toggle effects on/off.
        Affects *ALL* items that use that effect.
        Is not stateful.  Will reset if Pyfa is closed and reopened.
        """

        try:
            activeByDefault = getattr(self.item.effects[event.GetText()], "activeByDefault")
            if activeByDefault:
                setattr(self.item.effects[event.GetText()], "activeByDefault", False)
            else:
                setattr(self.item.effects[event.GetText()], "activeByDefault", True)

        except AttributeError:
            # Attribute doesn't exist, do nothing
            pass

        self.RefreshValues(event)

    @staticmethod
    def OnRightClick(event):
        """
        Debug use: open effect file with default application.
        If effect file does not exist, create it
        """

        file_ = os.path.join(config.pyfaPath, "eos", "effects", "%s.py" % event.GetText().lower())

        if not os.path.isfile(file_):
            open(file_, 'a').close()

        if 'wxMSW' in wx.PlatformInfo:
            os.startfile(file_)
        elif 'wxMac' in wx.PlatformInfo:
            os.system("open " + file_)
        else:
            subprocess.call(["xdg-open", file_])

    def RefreshValues(self, event):
        self.Freeze()
        self.effectList.ClearAll()
        self.PopulateList()
        self.effectList.RefreshRows()
        self.Layout()
        self.Thaw()
        event.Skip()


class ItemAffectedBy(wx.Panel):
    ORDER = [Fit, Ship, Citadel, Mode, Module, Drone, Fighter, Implant, Booster, Skill]

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.item = item

        self.activeFit = gui.mainFrame.MainFrame.getInstance().getActiveFit()

        self.showRealNames = False
        self.showAttrView = False
        self.expand = -1

        self.treeItems = []

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.affectedBy = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.NO_BORDER)
        mainSizer.Add(self.affectedBy, 1, wx.ALL | wx.EXPAND, 0)

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)

        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.toggleExpandBtn = wx.ToggleButton(self, wx.ID_ANY, u"Expand All", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleExpandBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.toggleNameBtn = wx.ToggleButton(self, wx.ID_ANY, u"Toggle Names", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleNameBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, u"Toggle View", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
            bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
            self.refreshBtn.Bind(wx.EVT_BUTTON, self.RefreshTree)

        self.toggleNameBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleNameMode)
        self.toggleExpandBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleExpand)
        self.toggleViewBtn.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleViewMode)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)
        self.SetSizer(mainSizer)
        self.PopulateTree()
        self.Layout()
        self.affectedBy.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.scheduleMenu)

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu, event.Item)

    def spawnMenu(self, item):
        self.affectedBy.SelectItem(item)

        stuff = self.affectedBy.GetPyData(item)
        # String is set as data when we are dealing with attributes, not stuff containers
        if stuff is None or isinstance(stuff, basestring):
            return
        contexts = []

        # Skills are different in that they don't have itemModifiedAttributes,
        # which is needed if we send the container to itemStats dialog. So
        # instead, we send the item.
        type_ = stuff.__class__.__name__
        contexts.append(("itemStats", type_))
        menu = ContextMenu.getMenu(stuff if type_ != "Skill" else stuff.item, *contexts)
        self.PopupMenu(menu)

    def ExpandCollapseTree(self):

        self.Freeze()
        if self.expand == 1:
            self.affectedBy.ExpandAll()
        else:
            try:
                self.affectedBy.CollapseAll()
            except:
                pass

        self.Thaw()

    def ToggleExpand(self, event):
        self.expand *= -1
        self.ExpandCollapseTree()

    def ToggleViewTree(self):
        self.Freeze()

        for item in self.treeItems:
            change = self.affectedBy.GetPyData(item)
            display = self.affectedBy.GetItemText(item)
            self.affectedBy.SetItemText(item, change)
            self.affectedBy.SetPyData(item, display)

        self.Thaw()

    def UpdateTree(self):
        self.Freeze()
        self.affectedBy.DeleteAllItems()
        self.PopulateTree()
        self.Thaw()

    def RefreshTree(self, event):
        self.UpdateTree()
        event.Skip()

    def ToggleViewMode(self, event):
        self.showAttrView = not self.showAttrView
        self.affectedBy.DeleteAllItems()
        self.PopulateTree()
        event.Skip()

    def ToggleNameMode(self, event):
        self.showRealNames = not self.showRealNames
        self.ToggleViewTree()
        event.Skip()

    def PopulateTree(self):
        # sheri was here
        del self.treeItems[:]
        root = self.affectedBy.AddRoot("WINPWNZ0R")
        self.affectedBy.SetPyData(root, None)

        self.imageList = wx.ImageList(16, 16)
        self.affectedBy.SetImageList(self.imageList)

        if self.showAttrView:
            self.buildAttributeView(root)
        else:
            self.buildModuleView(root)

        self.ExpandCollapseTree()

    def sortAttrDisplayName(self, attr):
        info = self.stuff.item.attributes.get(attr)
        if info and info.displayName != "":
            return info.displayName

        return attr

    def buildAttributeView(self, root):
        """
        We first build a usable dictionary of items. The key is either a fit
        if the afflictions stem from a projected fit, or self.stuff if they
        are local afflictions (everything else, even gang boosts at this time)
        The value of this is yet another dictionary in the following format:

        "attribute name": {
              "Module Name": [
                   class of affliction,
                   affliction item (required due to GH issue #335)
                   modifier type
                   amount of modification
                   whether this affliction was projected
              ]
        }
        """

        attributes = self.stuff.itemModifiedAttributes if self.item == self.stuff.item else self.stuff.chargeModifiedAttributes
        container = {}
        for attrName in attributes.iterAfflictions():
            # if value is 0 or there has been no change from original to modified, return
            if attributes[attrName] == (attributes.getOriginal(attrName, 0)):
                continue

            for fit, afflictors in attributes.getAfflictions(attrName).iteritems():
                for afflictor, modifier, amount, used in afflictors:

                    if not used or afflictor.item is None:
                        continue

                    if fit.ID != self.activeFit:
                        # affliction fit does not match our fit
                        if fit not in container:
                            container[fit] = {}
                        items = container[fit]
                    else:
                        # local afflictions
                        if self.stuff not in container:
                            container[self.stuff] = {}
                        items = container[self.stuff]

                    # items hold our module: info mappings
                    if attrName not in items:
                        items[attrName] = []

                    if afflictor == self.stuff and getattr(afflictor, 'charge', None):
                        # we are showing a charges modifications, see #335
                        item = afflictor.charge
                    else:
                        item = afflictor.item

                    items[attrName].append(
                            (type(afflictor), afflictor, item, modifier, amount, getattr(afflictor, "projected", False)))

        # Make sure projected fits are on top
        rootOrder = container.keys()
        rootOrder.sort(key=lambda x: self.ORDER.index(type(x)))

        # Now, we take our created dictionary and start adding stuff to our tree
        for thing in rootOrder:
            # This block simply directs which parent we are adding to (root or projected fit)
            if thing == self.stuff:
                parent = root
            else:  # projected fit
                icon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                child = self.affectedBy.AppendItem(root, "{} ({})".format(thing.name, thing.ship.item.name), icon)
                parent = child

            attributes = container[thing]
            attrOrder = sorted(attributes.keys(), key=self.sortAttrDisplayName)

            for attrName in attrOrder:
                attrInfo = self.stuff.item.attributes.get(attrName)
                displayName = attrInfo.displayName if attrInfo and attrInfo.displayName != "" else attrName

                if attrInfo:
                    if attrInfo.icon is not None:
                        iconFile = attrInfo.icon.iconFile
                        icon = BitmapLoader.getBitmap(iconFile, "icons")
                        if icon is None:
                            icon = BitmapLoader.getBitmap("transparent16x16", "gui")
                        attrIcon = self.imageList.Add(icon)
                    else:
                        attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))
                else:
                    attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))

                if self.showRealNames:
                    display = attrName
                    saved = displayName
                else:
                    display = displayName
                    saved = attrName

                # this is the attribute node
                child = self.affectedBy.AppendItem(parent, display, attrIcon)
                self.affectedBy.SetPyData(child, saved)
                self.treeItems.append(child)

                items = attributes[attrName]
                items.sort(key=lambda x: self.ORDER.index(x[0]))
                for itemInfo in items:
                    afflictorType, afflictor, item, attrModifier, attrAmount, projected = itemInfo

                    if afflictorType == Ship:
                        itemIcon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                    elif item.icon:
                        bitmap = BitmapLoader.getBitmap(item.icon.iconFile, "icons")
                        itemIcon = self.imageList.Add(bitmap) if bitmap else -1
                    else:
                        itemIcon = -1

                    displayStr = item.name

                    if projected:
                        displayStr += " (projected)"

                    if attrModifier == "s*":
                        attrModifier = "*"
                        penalized = "(penalized)"
                    else:
                        penalized = ""

                    # this is the Module node, the attribute will be attached to this
                    display = "%s %s %.2f %s" % (displayStr, attrModifier, attrAmount, penalized)
                    treeItem = self.affectedBy.AppendItem(child, display, itemIcon)
                    self.affectedBy.SetPyData(treeItem, afflictor)

    def buildModuleView(self, root):
        """
        We first build a usable dictionary of items. The key is either a fit
        if the afflictions stem from a projected fit, or self.stuff if they
        are local afflictions (everything else, even gang boosts at this time)
        The value of this is yet another dictionary in the following format:

        "Module Name": [
            class of affliction,
            set of afflictors (such as 2 of the same module),
            info on affliction (attribute name, modifier, and modification amount),
            item that will be used to determine icon (required due to GH issue #335)
            whether this affliction is actually used (unlearned skills are not used)
        ]
        """

        attributes = self.stuff.itemModifiedAttributes if self.item == self.stuff.item else self.stuff.chargeModifiedAttributes
        container = {}
        for attrName in attributes.iterAfflictions():
            # if value is 0 or there has been no change from original to modified, return
            if attributes[attrName] == (attributes.getOriginal(attrName, 0)):
                continue

            for fit, afflictors in attributes.getAfflictions(attrName).iteritems():
                for afflictor, modifier, amount, used in afflictors:
                    if not used or getattr(afflictor, 'item', None) is None:
                        continue

                    if fit.ID != self.activeFit:
                        # affliction fit does not match our fit
                        if fit not in container:
                            container[fit] = {}
                        items = container[fit]
                    else:
                        # local afflictions
                        if self.stuff not in container:
                            container[self.stuff] = {}
                        items = container[self.stuff]

                    if afflictor == self.stuff and getattr(afflictor, 'charge', None):
                        # we are showing a charges modifications, see #335
                        item = afflictor.charge
                    else:
                        item = afflictor.item

                    # items hold our module: info mappings
                    if item.name not in items:
                        items[item.name] = [type(afflictor), set(), [], item, getattr(afflictor, "projected", False)]

                    info = items[item.name]
                    info[1].add(afflictor)
                    # If info[1] > 1, there are two separate modules working.
                    # Check to make sure we only include the modifier once
                    # See GH issue 154
                    if len(info[1]) > 1 and (attrName, modifier, amount) in info[2]:
                        continue
                    info[2].append((attrName, modifier, amount))

        # Make sure projected fits are on top
        rootOrder = container.keys()
        rootOrder.sort(key=lambda x: self.ORDER.index(type(x)))

        # Now, we take our created dictionary and start adding stuff to our tree
        for thing in rootOrder:
            # This block simply directs which parent we are adding to (root or projected fit)
            if thing == self.stuff:
                parent = root
            else:  # projected fit
                icon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                child = self.affectedBy.AppendItem(root, "{} ({})".format(thing.name, thing.ship.item.name), icon)
                parent = child

            items = container[thing]
            order = items.keys()
            order.sort(key=lambda x: (self.ORDER.index(items[x][0]), x))

            for itemName in order:
                info = items[itemName]
                afflictorType, afflictors, attrData, item, projected = info
                counter = len(afflictors)
                if afflictorType == Ship:
                    itemIcon = self.imageList.Add(BitmapLoader.getBitmap("ship_small", "gui"))
                elif item.icon:
                    bitmap = BitmapLoader.getBitmap(item.icon.iconFile, "icons")
                    itemIcon = self.imageList.Add(bitmap) if bitmap else -1
                else:
                    itemIcon = -1

                displayStr = itemName

                if counter > 1:
                    displayStr += " x {}".format(counter)

                if projected:
                    displayStr += " (projected)"

                # this is the Module node, the attribute will be attached to this
                child = self.affectedBy.AppendItem(parent, displayStr, itemIcon)
                self.affectedBy.SetPyData(child, afflictors.pop())

                if counter > 0:
                    attributes = []
                    for attrName, attrModifier, attrAmount in attrData:
                        attrInfo = self.stuff.item.attributes.get(attrName)
                        displayName = attrInfo.displayName if attrInfo else ""

                        if attrInfo:
                            if attrInfo.icon is not None:
                                iconFile = attrInfo.icon.iconFile
                                icon = BitmapLoader.getBitmap(iconFile, "icons")
                                if icon is None:
                                    icon = BitmapLoader.getBitmap("transparent16x16", "gui")

                                attrIcon = self.imageList.Add(icon)
                            else:
                                attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))
                        else:
                            attrIcon = self.imageList.Add(BitmapLoader.getBitmap("7_15", "icons"))

                        if attrModifier == "s*":
                            attrModifier = "*"
                            penalized = "(penalized)"
                        else:
                            penalized = ""

                        attributes.append((attrName, (displayName if displayName != "" else attrName), attrModifier,
                                           attrAmount, penalized, attrIcon))

                    attrSorted = sorted(attributes, key=lambda attribName: attribName[0])
                    for attr in attrSorted:
                        attrName, displayName, attrModifier, attrAmount, penalized, attrIcon = attr

                        if self.showRealNames:
                            display = "%s %s %.2f %s" % (attrName, attrModifier, attrAmount, penalized)
                            saved = "%s %s %.2f %s" % (
                                displayName if displayName != "" else attrName,
                                attrModifier,
                                attrAmount,
                                penalized
                            )
                        else:
                            display = "%s %s %.2f %s" % (
                                displayName if displayName != "" else attrName,
                                attrModifier,
                                attrAmount,
                                penalized
                            )
                            saved = "%s %s %.2f %s" % (attrName, attrModifier, attrAmount, penalized)

                        treeitem = self.affectedBy.AppendItem(child, display, attrIcon)
                        self.affectedBy.SetPyData(treeitem, saved)
                        self.treeItems.append(treeitem)


class ItemProperties(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.paramList = AutoListCtrl(self, wx.ID_ANY,
                                      style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.NO_BORDER)
        mainSizer.Add(self.paramList, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self.toggleView = 1
        self.stuff = stuff
        self.item = item
        self.attrInfo = {}
        self.attrValues = {}
        self._fetchValues()

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)
        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.totalAttrsLabel = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        mainSizer.Add(bSizer, 0, wx.ALIGN_RIGHT)

        self.PopulateList()

    def _fetchValues(self):
        if self.stuff is None:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.item.attributes)
            self.attrValues.update(self.item.attributes)
        elif self.stuff.item == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.item.attributes)
            self.attrValues.update(self.stuff.itemModifiedAttributes)
        elif self.stuff.charge == self.item:
            self.attrInfo.clear()
            self.attrValues.clear()
            self.attrInfo.update(self.stuff.charge.attributes)
            self.attrValues.update(self.stuff.chargeModifiedAttributes)
        # When item for stats window no longer exists, don't change anything
        else:
            return

    def PopulateList(self):
        self.paramList.InsertColumn(0, "Attribute")
        self.paramList.InsertColumn(1, "Current Value")
        self.paramList.SetColumnWidth(0, 110)
        self.paramList.SetColumnWidth(1, 1500)
        self.paramList.setResizeColumn(0)

        if self.stuff:
            names = dir(self.stuff)
        else:
            names = dir(self.item)

        names = [a for a in names if not (a.startswith('__') and a.endswith('__'))]

        idNameMap = {}
        idCount = 0
        for name in names:
            try:
                if self.stuff:
                    attrName = name.title()
                    value = getattr(self.stuff, name)
                else:
                    attrName = name.title()
                    value = getattr(self.item, name)
            except Exception as e:
                # TODO: Add logging to this.
                # We couldn't get a property for some reason. Skip it for now.
                print(e)
                continue

            index = self.paramList.InsertStringItem(sys.maxint, attrName)
            # index = self.paramList.InsertImageStringItem(sys.maxint, attrName)
            idNameMap[idCount] = attrName
            self.paramList.SetItemData(index, idCount)
            idCount += 1

            valueUnit = str(value)

            self.paramList.SetStringItem(index, 1, valueUnit)

        self.paramList.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
        self.paramList.RefreshRows()
        self.totalAttrsLabel.SetLabel("%d attributes. " % idCount)
        self.Layout()
