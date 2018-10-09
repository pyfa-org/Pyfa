import csv
import config

# noinspection PyPackageRequirements
import wx
import wx.lib.agw.hypertreelist
from gui.builtinItemStatsViews.helpers import AutoListCtrl


from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


class ItemParams(wx.Panel):
    def __init__(self, parent, stuff, item, context=None):
        wx.Panel.__init__(self, parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.paramList = wx.lib.agw.hypertreelist.HyperTreeList(self, wx.ID_ANY, agwStyle=wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT)

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

        self.totalAttrsLabel = wx.StaticText(self, wx.ID_ANY, " ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.totalAttrsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT)

        self.toggleViewBtn = wx.ToggleButton(self, wx.ID_ANY, "Toggle view mode", wx.DefaultPosition, wx.DefaultSize,
                                             0)
        bSizer.Add(self.toggleViewBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        self.exportStatsBtn = wx.ToggleButton(self, wx.ID_ANY, "Export Item Stats", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        bSizer.Add(self.exportStatsBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        if stuff is not None:
            self.refreshBtn = wx.Button(self, wx.ID_ANY, "Refresh", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
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
        if event:
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

        with open(saveFileDialog.GetPath(), "w") as exportFile:
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
        self.paramList.AddColumn("Attribute")
        self.paramList.AddColumn("Current Value")
        if self.stuff is not None:
            self.paramList.AddColumn("Base Value")

        self.paramList.SetMainColumn(0)  # the one with the tree in it...
        self.paramList.SetColumnWidth(0, 175)

        root = self.paramList.AddRoot("The Root Item")
        # self.paramList.setResizeColumn(0)
        self.imageList = wx.ImageList(16, 16)
        self.paramList.AssignImageList(self.imageList)

        names = list(self.attrValues.keys())
        names.sort()

        idNameMap = {}
        idCount = 0
        for name in names:
            info = self.attrInfo.get(name)
            att = self.attrValues[name]

            # If we're working with a stuff object, we should get the original value from our getBaseAttrValue function,
            # which will return the value with respect to the effective base (with mutators / overrides in place)
            valDefault = getattr(info, "value", None)  # Get default value from attribute
            if self.stuff is not None:
                # if it's a stuff, overwrite default (with fallback to current value)
                valDefault = self.stuff.getBaseAttrValue(name, valDefault)
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
                if info.iconID is not None:
                    iconFile = info.iconID
                    icon = BitmapLoader.getBitmap(iconFile, "icons")

                    if icon is None:
                        icon = BitmapLoader.getBitmap("transparent16x16", "gui")

                    attrIcon = self.imageList.Add(icon)
                else:
                    attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))
            else:
                attrIcon = self.imageList.Add(BitmapLoader.getBitmap("0", "icons"))

            index = self.paramList.AppendItem(root, attrName)
            idNameMap[idCount] = attrName
            self.paramList.SetPyData(index, idCount)
            idCount += 1

            if self.toggleView != 1:
                valueUnit = str(value)
            elif info and info.unit:
                valueUnit = self.FormatValue(*info.unit.TranslateValue(value))
            else:
                valueUnit = formatAmount(value, 3, 0, 0)

            if self.toggleView != 1:
                valueUnitDefault = str(valueDefault)
            elif info and info.unit:
                valueUnitDefault = self.FormatValue(*info.unit.TranslateValue(valueDefault))
            else:
                valueUnitDefault = formatAmount(valueDefault, 3, 0, 0)

            self.paramList.SetItemText(index, valueUnit, 1)
            if self.stuff is not None:
                self.paramList.SetItemText(index, valueUnitDefault,2)
            self.paramList.SetItemImage(index, attrIcon, which=wx.TreeItemIcon_Normal)
        # @todo: pheonix, this lamda used cmp() which no longer exists in py3. Probably a better way to do this in the
        # long run, take a look


        # self.paramList.SortItems(lambda id1, id2: (idNameMap[id1] > idNameMap[id2]) - (idNameMap[id1] < idNameMap[id2]))
        # self.paramList.RefreshRows()
        self.totalAttrsLabel.SetLabel("%d attributes. " % idCount)

        self.Layout()

    @staticmethod
    def FormatValue(value, unit):
        """Formats a value / unit combination into a string
        @todo: move this to a more central location, since this is also used in the item mutator panel"""
        if isinstance(value, (int, float)):
            fvalue = formatAmount(value, 3, 0, 0)
        else:
            fvalue = value
        return "%s %s" % (fvalue, unit)



if __name__ == "__main__":

    import eos.db
    # need to set up some paths, since bitmap loader requires config to have things
    # Should probably change that so that it's not dependant on config
    import os
    os.chdir('..')
    import config
    config.defPaths(None)

    class Frame(wx.Frame):
        def __init__(self, title):
            super().__init__(None, title=title, size=(1000, 500))

            if 'wxMSW' in wx.PlatformInfo:
                color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
                self.SetBackgroundColour(color)

            main_sizer = wx.BoxSizer(wx.HORIZONTAL)

            item = eos.db.getItem(23773)  # Ragnarok

            panel = ItemParams(self, None, item)


            main_sizer.Add(panel, 1, wx.EXPAND | wx.ALL, 2)

            self.SetSizer(main_sizer)

    app = wx.App(redirect=False)   # Error messages go to popup window
    top = Frame("Test Item Attributes")
    top.Show()
    app.MainLoop()
