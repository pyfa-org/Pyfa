# =============================================================================
# Copyright (C) 2010 Lucas Thode
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


# noinspection PyPackageRequirements
import wx
from service.port.eft import EFT_OPTIONS
from service.settings import SettingsProvider


class CopySelectDialog(wx.Dialog):
    copyFormatEft = 0
    copyFormatXml = 1
    copyFormatDna = 2
    copyFormatEsi = 3
    copyFormatMultiBuy = 4
    copyFormatEfs = 5

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Select a format", size=(-1, -1),
                           style=wx.DEFAULT_DIALOG_STYLE)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.settings = SettingsProvider.getInstance().getSettings("pyfaExport", {"format": 0, "options": 0})

        self.copyFormats = {
            "EFT": CopySelectDialog.copyFormatEft,
            "XML": CopySelectDialog.copyFormatXml,
            "DNA": CopySelectDialog.copyFormatDna,
            "ESI": CopySelectDialog.copyFormatEsi,
            "MultiBuy": CopySelectDialog.copyFormatMultiBuy,
            "EFS": CopySelectDialog.copyFormatEfs
        }

        for i, format in enumerate(self.copyFormats.keys()):
            if i == 0:
                rdo = wx.RadioButton(self, wx.ID_ANY, format, style=wx.RB_GROUP)
            else:
                rdo = wx.RadioButton(self, wx.ID_ANY, format)
            rdo.Bind(wx.EVT_RADIOBUTTON, self.Selected)
            if self.settings['format'] == self.copyFormats[format]:
                rdo.SetValue(True)
                self.copyFormat = self.copyFormats[format]
            mainSizer.Add(rdo, 0, wx.EXPAND | wx.ALL, 5)

        # some sizer magic to deal with https://github.com/wxWidgets/Phoenix/issues/974
        self.box1 = wx.StaticBox(self, -1, "EFT Options")
        self.bsizer1 = wx.BoxSizer(wx.VERTICAL)
        self.bsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.bsizer1.AddSpacer(10)

        self.bsizer1.Add(self.bsizer2, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.options = {}

        for x, v in EFT_OPTIONS.items():
            ch = wx.CheckBox(self.box1, -1, v['name'])
            self.options[x] = ch
            if self.settings['options'] & x:
                ch.SetValue(True)
            self.bsizer2.Add(ch, 1, wx.EXPAND)

        self.box1.SetSizer(self.bsizer1)

        mainSizer.Add(self.box1, 0, wx.EXPAND | wx.ALL, 5)
        buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if buttonSizer:
            mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.box1.Show(self.GetSelected() == CopySelectDialog.copyFormatEft)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Center()

    def Selected(self, event):
        obj = event.GetEventObject()
        format = obj.GetLabel()
        self.box1.Show(format == "EFT")
        self.Fit()
        self.copyFormat = self.copyFormats[format]

    def GetSelected(self):
        return self.copyFormat

    def GetOptions(self):
        i = 0
        for x, v in self.options.items():
            if v.IsChecked():
                i = i ^ x
        return i

