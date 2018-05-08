import os
import subprocess
import config

# noinspection PyPackageRequirements
import wx

from .helpers import AutoListCtrl


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
        names = list(effects.keys())
        names.sort()

        for name in names:
            index = self.effectList.InsertItem(self.effectList.GetItemCount(), name)

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

            self.effectList.SetItem(index, 1, activeByDefault)
            self.effectList.SetItem(index, 2, effectTypeText)
            if config.debug:
                self.effectList.SetItem(index, 3, effectRunTime)
                self.effectList.SetItem(index, 4, str(effects[name].ID))

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
