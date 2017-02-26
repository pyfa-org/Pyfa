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


class CopySelectDialog(wx.Dialog):
    copyFormatEft = 0
    copyFormatEftImps = 1
    copyFormatXml = 2
    copyFormatDna = 3
    copyFormatCrest = 4
    copyFormatMultiBuy = 5

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Select a format", size=(-1, -1),
                           style=wx.DEFAULT_DIALOG_STYLE)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        copyFormats = [u"EFT", u"EFT (Implants)", u"XML", u"DNA", u"CREST", u"MultiBuy"]
        copyFormatTooltips = {CopySelectDialog.copyFormatEft: u"EFT text format",
                              CopySelectDialog.copyFormatEftImps: u"EFT text format",
                              CopySelectDialog.copyFormatXml: u"EVE native XML format",
                              CopySelectDialog.copyFormatDna: u"A one-line text format",
                              CopySelectDialog.copyFormatCrest: u"A JSON format used for EVE CREST",
                              CopySelectDialog.copyFormatMultiBuy: u"MultiBuy text format"}
        selector = wx.RadioBox(self, wx.ID_ANY, label=u"Copy to the clipboard using:", choices=copyFormats,
                               style=wx.RA_SPECIFY_ROWS)
        selector.Bind(wx.EVT_RADIOBOX, self.Selected)
        for format, tooltip in copyFormatTooltips.iteritems():
            selector.SetItemToolTip(format, tooltip)

        self.copyFormat = CopySelectDialog.copyFormatEft
        selector.SetSelection(self.copyFormat)

        mainSizer.Add(selector, 0, wx.EXPAND | wx.ALL, 5)

        buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if buttonSizer:
            mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mainSizer)
        self.Fit()
        self.Center()

    def Selected(self, event):
        self.copyFormat = event.GetSelection()

    def GetSelected(self):
        return self.copyFormat
