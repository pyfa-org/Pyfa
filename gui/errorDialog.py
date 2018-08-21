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

# import platform
import sys
#
# noinspection PyPackageRequirements
import wx
import traceback
import config
from logbook import Logger
from service.prereqsCheck import version_block

pyfalog = Logger(__name__)


class ErrorHandler(object):
    __parent = None
    __frame = None

    @classmethod
    def HandleException(cls, exc_type, exc_value, exc_traceback):
        with config.logging_setup.threadbound():
            # Print the base level traceback
            t = traceback.format_exception(exc_type, exc_value, exc_traceback)
            pyfalog.critical("\n\n" + "".join(t))

            if cls.__parent is None:
                app = wx.App(False)
                cls.__frame = ErrorFrame(None)
                cls.__frame.addException("".join(t))
                app.MainLoop()
                sys.exit()
            else:
                if not cls.__frame:
                    cls.__frame = ErrorFrame(cls.__parent)
                cls.__frame.Show()
                cls.__frame.addException("".join(t))

    @classmethod
    def SetParent(cls, parent):
        cls.__parent = parent


class ErrorFrame(wx.Frame):
    def __init__(self, parent=None, error_title='Error!'):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="pyfa error", pos=wx.DefaultPosition, size=wx.Size(500, 600),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.STAY_ON_TOP)

        desc = "pyfa has experienced an unexpected issue. Below is a message that contains crucial\n" \
               "information about how this was triggered. Please contact the developers with the\n" \
               "information provided through the EVE Online forums or file a GitHub issue."

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

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

        # github = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.ID_ANY, label="Github", URL="https://github.com/pyfa-org/Pyfa/issues")
        # box.Add(github, 0, wx.ALL, 5)
        #
        # eveForums = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.ID_ANY, label="EVE Forums", URL="https://forums.eveonline.com/t/27156")
        # box.Add(eveForums, 0, wx.ALL, 5)

        # mainSizer.AddSpacer((0, 5), 0, wx.EXPAND, 5)

        self.errorTextCtrl = wx.TextCtrl(self, wx.ID_ANY, version_block.strip(), wx.DefaultPosition,
                                         (-1, 400), wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_DONTWRAP)
        self.errorTextCtrl.SetFont(wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))
        mainSizer.Add(self.errorTextCtrl, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER, 5)
        self.errorTextCtrl.AppendText("\n")
        self.errorTextCtrl.Layout()

        self.SetSizer(mainSizer)
        mainSizer.Layout()
        self.Layout()

        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show()

    def OnClose(self, evt):
        self.Hide()

    def addException(self, text):
        self.errorTextCtrl.AppendText("\n{}\n\n{}".format("#" * 20, text))
