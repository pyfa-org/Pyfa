# ===============================================================================
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
# ===============================================================================

import platform
import sys

# noinspection PyPackageRequirements
import wx

try:
    import config
except:
    config = None

try:
    import sqlalchemy

    sqlalchemy_version = sqlalchemy.__version__
except:
    sqlalchemy_version = "Unknown"

try:
    from logbook import __version__ as logbook_version
except:
    logbook_version = "Unknown"


class ErrorFrame(wx.Frame):
    def __init__(self, exception=None, tb=None, error_title='Error!'):
        v = sys.version_info

        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="pyfa error", pos=wx.DefaultPosition, size=wx.Size(500, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.STAY_ON_TOP)

        desc = "pyfa has experienced an unexpected issue. Below is a message that contains crucial\n" \
               "information about how this was triggered. Please contact the developers with the\n" \
               "information provided through the EVE Online forums or file a GitHub issue."

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        headSizer = wx.BoxSizer(wx.HORIZONTAL)

        headingText = wx.StaticText(self, wx.ID_ANY, error_title, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        headingText.SetFont(wx.Font(14, 74, 90, 92, False))

        headSizer.Add(headingText, 1, wx.ALL, 5)
        mainSizer.Add(headSizer, 0, wx.EXPAND, 5)

        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND | wx.ALL, 5)

        box = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(box, 0, wx.EXPAND | wx.ALIGN_TOP)

        descText = wx.StaticText(self, wx.ID_ANY, desc)
        box.Add(descText, 1, wx.ALL, 5)

        github = wx.HyperlinkCtrl(self, wx.ID_ANY, "Github", "https://github.com/pyfa-org/Pyfa/issues",
                                  wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE)
        box.Add(github, 0, wx.ALL, 5)

        eveForums = wx.HyperlinkCtrl(self, wx.ID_ANY, "EVE Forums", "https://forums.eveonline.com/default.aspx?g=posts&t=466425",
                                     wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE)
        box.Add(eveForums, 0, wx.ALL, 5)

        # mainSizer.AddSpacer((0, 5), 0, wx.EXPAND, 5)

        errorTextCtrl = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (-1, 400), wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_DONTWRAP)
        errorTextCtrl.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        mainSizer.Add(errorTextCtrl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 5)

        try:
            errorTextCtrl.AppendText("OS version: \t" + str(platform.platform()))
        except:
            errorTextCtrl.AppendText("OS version: Unknown")
        errorTextCtrl.AppendText("\n")

        try:
            errorTextCtrl.AppendText("Python: \t" + '{}.{}.{}'.format(v.major, v.minor, v.micro))
        except:
            errorTextCtrl.AppendText("Python: Unknown")
        errorTextCtrl.AppendText("\n")

        try:
            errorTextCtrl.AppendText("wxPython: \t" + wx.VERSION_STRING)
        except:
            errorTextCtrl.AppendText("wxPython: Unknown")
        errorTextCtrl.AppendText("\n")

        errorTextCtrl.AppendText("SQLAlchemy: \t" + str(sqlalchemy_version))
        errorTextCtrl.AppendText("\n")

        errorTextCtrl.AppendText("Logbook: \t" + str(logbook_version))
        errorTextCtrl.AppendText("\n")

        try:
            errorTextCtrl.AppendText("pyfa version: {0} {1} - {2} {3}".format(config.version, config.tag, config.expansionName, config.expansionVersion))
        except:
            errorTextCtrl.AppendText("pyfa version: Unknown")
        errorTextCtrl.AppendText('\n')

        errorTextCtrl.AppendText("pyfa root: " + str(config.pyfaPath or "Unknown"))
        errorTextCtrl.AppendText('\n')
        errorTextCtrl.AppendText("save path: " + str(config.savePath or "Unknown"))
        errorTextCtrl.AppendText('\n')
        errorTextCtrl.AppendText("fs encoding: " + str(sys.getfilesystemencoding() or "Unknown"))
        errorTextCtrl.AppendText('\n\n')

        errorTextCtrl.AppendText("EXCEPTION: " + str(exception or "Unknown"))
        errorTextCtrl.AppendText('\n\n')

        if tb:
            for line in tb:
                errorTextCtrl.AppendText(line)
        errorTextCtrl.Layout()

        self.SetSizer(mainSizer)
        mainSizer.Layout()
        self.Layout()

        self.Centre(wx.BOTH)

        self.Show()
