#===============================================================================
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
#===============================================================================

import wx

class ImportDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Import fitting from ...", pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        headerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.cFilePicker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a fit file", u"*.*", style=wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST)
        headerSizer.Add(self.cFilePicker, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnImportEveXML = wx.Button(self, wx.ID_ANY, u"Import from EVE", wx.DefaultPosition, wx.DefaultSize, 0)
        headerSizer.Add(self.btnImportEveXML, 0, wx.TOP | wx.BOTTOM | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer.Add(headerSizer, 0, wx.EXPAND, 5)

        contentSizer = wx.BoxSizer(wx.VERTICAL)

        self.tcPreview = wx.TextCtrl(self, wx.ID_ANY, u"THIS IS AN EFT FIT PREVIEW | log", style=wx.TE_READONLY)
        contentSizer.Add(self.tcPreview, 1, wx.EXPAND, 5)

        mainSizer.Add(contentSizer, 1, wx.EXPAND, 5)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ckbPreview = wx.CheckBox(self, wx.ID_ANY, u"Preview")
        footerSizer.Add(self.ckbPreview, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.btnOK, 0, wx.ALL, 5)

        mainSizer.Add(footerSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)



class ExportDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Export fit as ...", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        fileSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.fitFileName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fileSizer.Add(self.fitFileName, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.cDirPicker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DIR_MUST_EXIST)
        fileSizer.Add(self.cDirPicker, 0, wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        fileSizer.Add(self.btnOK, 0, wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer.Add(fileSizer, 0, wx.EXPAND, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        choiceSizer = wx.BoxSizer(wx.VERTICAL)

        chCtrlChoices = [ u"EFT file", u"XML file", u"EFT && XML file" ]
        self.chCtrl = wx.RadioBox(self, wx.ID_ANY, u"Choose wisely", wx.DefaultPosition, wx.DefaultSize, chCtrlChoices, 2, wx.RA_SPECIFY_COLS)
        self.chCtrl.SetSelection(0)
        choiceSizer.Add(self.chCtrl, 0, wx.EXPAND | wx.ALL, 5)

        mainSizer.Add(choiceSizer, 1, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        mainSizer.Fit(self)

        self.Centre(wx.BOTH)
