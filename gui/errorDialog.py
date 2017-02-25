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
import sys
import gui.utils.fonts as fonts
import config

class ErrorFrame(wx.Frame):

    def __init__(self, exception, tb):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="pyfa error", pos=wx.DefaultPosition, size=wx.Size(500, 400), style=wx.DEFAULT_FRAME_STYLE^ wx.RESIZE_BORDER|wx.STAY_ON_TOP)

        desc =  "pyfa has experienced an unexpected error. Below is the " \
                "Traceback that contains crucial information about how this " \
                "error was triggered. Please contact the developers with " \
                "the information provided through the EVE Online forums " \
                "or file a GitHub issue."

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        headSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.headingText = wx.StaticText(self, wx.ID_ANY, "Error!", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.headingText.SetFont(wx.Font(14, 74, 90, 92, False))

        headSizer.Add(self.headingText, 1, wx.ALL, 5)
        mainSizer.Add(headSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND |wx.ALL, 5)

        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.descText = wx.TextCtrl( self, wx.ID_ANY, desc, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE|wx.TRANSPARENT_WINDOW )
        self.descText.SetFont(wx.Font(fonts.BIG, wx.SWISS, wx.NORMAL, wx.NORMAL))
        descSizer.Add(self.descText, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(descSizer, 0, wx.EXPAND, 5)

        #mainSizer.AddSpacer((0, 5), 0, wx.EXPAND, 5)

        self.errorTextCtrl = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_DONTWRAP)
        self.errorTextCtrl.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        mainSizer.Add(self.errorTextCtrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        self.errorTextCtrl.AppendText("pyfa root: ")
        self.errorTextCtrl.AppendText(config.pyfaPath)
        self.errorTextCtrl.AppendText('\n')
        self.errorTextCtrl.AppendText("save path: ")
        self.errorTextCtrl.AppendText(config.savePath)
        self.errorTextCtrl.AppendText('\n')
        self.errorTextCtrl.AppendText("fs encoding: ")
        self.errorTextCtrl.AppendText(sys.getfilesystemencoding())
        self.errorTextCtrl.AppendText('\n\n')
        self.errorTextCtrl.AppendText(tb)

        self.SetSizer(mainSizer)
        mainSizer.Layout()
        self.Layout()

        self.Centre(wx.BOTH)

        self.Show()