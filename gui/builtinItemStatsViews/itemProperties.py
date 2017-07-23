import sys

# noinspection PyPackageRequirements
import wx

from helpers import AutoListCtrl


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

                index = self.paramList.InsertStringItem(sys.maxint, attrName)
                # index = self.paramList.InsertImageStringItem(sys.maxint, attrName)
                idNameMap[idCount] = attrName
                self.paramList.SetItemData(index, idCount)
                idCount += 1

                valueUnit = str(value)

                self.paramList.SetStringItem(index, 1, valueUnit)
            except:
                # TODO: Add logging to this.
                # We couldn't get a property for some reason. Skip it for now.
                continue

        self.paramList.SortItems(lambda id1, id2: cmp(idNameMap[id1], idNameMap[id2]))
        self.paramList.RefreshRows()
        self.totalAttrsLabel.SetLabel("%d attributes. " % idCount)
        self.Layout()
