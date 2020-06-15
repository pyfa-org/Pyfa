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

from eos.db import getFit
from gui.utils.clipboard import toClipboard
from service.const import PortMultiBuyOptions
from service.port import EfsPort, Port
from service.port.dna import DNA_OPTIONS
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
    copyFormatFitStats = 6

    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, title="Select a format", size=(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.CopySelectDict = {
            CopySelectDialog.copyFormatEft     : self.exportEft,
            CopySelectDialog.copyFormatXml     : self.exportXml,
            CopySelectDialog.copyFormatDna     : self.exportDna,
            CopySelectDialog.copyFormatEsi     : self.exportEsi,
            CopySelectDialog.copyFormatMultiBuy: self.exportMultiBuy,
            CopySelectDialog.copyFormatEfs     : self.exportEfs,
            CopySelectDialog.copyFormatFitStats: self.exportFitStats
        }

        self.mainFrame = parent
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.copyFormats = OrderedDict((
            ("EFT", (CopySelectDialog.copyFormatEft, EFT_OPTIONS)),
            ("MultiBuy", (CopySelectDialog.copyFormatMultiBuy, MULTIBUY_OPTIONS)),
            ("ESI", (CopySelectDialog.copyFormatEsi, None)),
            ("DNA", (CopySelectDialog.copyFormatDna, DNA_OPTIONS)),
            ("EFS", (CopySelectDialog.copyFormatEfs, None)),
            ("Stats", (CopySelectDialog.copyFormatFitStats, None)),
            # ("XML", (CopySelectDialog.copyFormatXml, None)),
        ))

        defaultFormatOptions = {}
        for formatId, formatOptions in self.copyFormats.values():
            if formatOptions is None:
                continue
            defaultFormatOptions[formatId] = {opt[0]: opt[3] for opt in formatOptions}

        self.settings = SettingsProvider.getInstance().getSettings("pyfaExport", {"format": self.copyFormatEft, "options": defaultFormatOptions})
        # Options used to be stored as int (EFT export options only),
        # overwrite them with new format when needed
        if isinstance(self.settings["options"], int):
            self.settings["options"] = defaultFormatOptions

        self.options = {}

        initialized = False
        self.copyFormat = self.copyFormatEft
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
                    if optDesc:
                        checkbox.SetToolTip(wx.ToolTip(optDesc))
                    self.options[formatId][optId] = checkbox
                    if self.settings['options'].get(formatId, {}).get(optId, defaultFormatOptions.get(formatId, {}).get(optId)):
                        checkbox.SetValue(True)
                    bsizer.Add(checkbox, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
                mainSizer.Add(bsizer, 0, wx.EXPAND | wx.LEFT, 20)

        buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if buttonSizer:
            mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.toggleOptions()
        self.SetSizer(mainSizer)
        self.Fit()
        self.Center()

    def Validate(self):
        # Since this dialog is shown through as ShowModal(),
        # we hook into the Validate function to veto the closing of the dialog until we're ready.
        # This always returns False, and when we're ready will EndModal()
        selected = self.GetSelected()
        options = self.GetOptions()

        settings = SettingsProvider.getInstance().getSettings("pyfaExport")
        settings["format"] = selected
        settings["options"] = options
        self.waitDialog = None

        def cb(text):
            if self.waitDialog:
                del self.waitDialog
            toClipboard(text)
            self.EndModal(wx.ID_OK)

        export_options = options.get(selected)
        if selected == CopySelectDialog.copyFormatMultiBuy and export_options.get(PortMultiBuyOptions.OPTIMIZE_PRICES, False):
            self.waitDialog = wx.BusyInfo("Optimizing Prices", parent=self)

        self.CopySelectDict[selected](export_options, callback=cb)

        return False

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

    def exportEft(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportEft(fit, options, callback)

    def exportDna(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportDna(fit, options, callback)

    def exportEsi(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportESI(fit, True, callback)

    def exportXml(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportXml([fit], None, callback)

    def exportMultiBuy(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportMultiBuy(fit, options, callback)

    def exportEfs(self, options, callback):
        fit = getFit(self.mainFrame.getActiveFit())
        EfsPort.exportEfs(fit, 0, callback)

    # noinspection PyUnusedLocal
    def exportFitStats(self, options, callback):
        """ Puts fit stats in textual format into the clipboard """
        fit = getFit(self.mainFrame.getActiveFit())
        Port.exportFitStats(fit, callback)

