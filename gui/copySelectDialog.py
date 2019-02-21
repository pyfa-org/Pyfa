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


from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

from service.port.eft import EFT_OPTIONS
from service.port.multibuy import MULTIBUY_OPTIONS
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

        self.copyFormats = OrderedDict((
            ("EFT", (CopySelectDialog.copyFormatEft, EFT_OPTIONS)),
            ("MultiBuy", (CopySelectDialog.copyFormatMultiBuy, MULTIBUY_OPTIONS)),
            ("ESI", (CopySelectDialog.copyFormatEsi, None)),
            ("EFS", (CopySelectDialog.copyFormatEfs, None)),
            # ("XML", (CopySelectDialog.copyFormatXml, None)),
            # ("DNA", (CopySelectDialog.copyFormatDna, None)),
        ))

        defaultFormatOptions = {}
        for formatId, formatOptions in self.copyFormats.values():
            if formatOptions is None:
                continue
            defaultFormatOptions[formatId] = {opt[0]: opt[3] for opt in formatOptions}

        self.settings = SettingsProvider.getInstance().getSettings("pyfaExport", {"format": 0, "options": defaultFormatOptions})

        self.options = {}

        initialized = False
        for formatName, formatData in self.copyFormats.items():
            formatId, formatOptions = formatData
            if not initialized:
                rdo = wx.RadioButton(self, wx.ID_ANY, formatName, style=wx.RB_GROUP)
                initialized = True
            else:
                rdo = wx.RadioButton(self, wx.ID_ANY, formatName)
            rdo.Bind(wx.EVT_RADIOBUTTON, self.Selected)
            if self.settings['format'] == formatId:
                rdo.SetValue(True)
                self.copyFormat = formatId
            mainSizer.Add(rdo, 0, wx.EXPAND | wx.ALL, 5)

            if formatOptions:
                bsizer = wx.BoxSizer(wx.VERTICAL)
                self.options[formatId] = {}

                for optId, optName, optDesc, _ in formatOptions:
                    checkbox = wx.CheckBox(self, -1, optName)
                    self.options[formatId][optId] = checkbox
                    if self.settings['options'].get(formatId, {}).get(optId, defaultFormatOptions.get(formatId, {}).get(optId)):
                        checkbox.SetValue(True)
                    bsizer.Add(checkbox, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
                mainSizer.Add(bsizer, 1, wx.EXPAND | wx.LEFT, 20)

        buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if buttonSizer:
            mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.toggleOptions()
        self.SetSizer(mainSizer)
        self.Fit()
        self.Center()

    def Selected(self, event):
        obj = event.GetEventObject()
        formatName = obj.GetLabel()
        self.copyFormat = self.copyFormats[formatName][0]
        self.toggleOptions()
        self.Fit()

    def toggleOptions(self):
        for formatId in self.options:
            for checkbox in self.options[formatId].values():
                checkbox.Enable(self.GetSelected() == formatId)

    def GetSelected(self):
        return self.copyFormat

    def GetOptions(self):
        options = {}
        for formatId in self.options:
            options[formatId] = {optId: ch.IsChecked() for optId, ch in self.options[formatId].items()}
        return options
