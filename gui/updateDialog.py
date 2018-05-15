# =============================================================================
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
# =============================================================================

# noinspection PyPackageRequirements
import wx
# noinspection PyPackageRequirements
import dateutil.parser
from service.settings import UpdateSettings as svc_UpdateSettings
import wx.html2
import webbrowser
import re
import markdown2

# HTML template. We link to a bootstrap cdn for quick and easy css, and include some additional teaks.
html_tmpl = """
<link href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' rel='stylesheet' />
<style>
body {{ padding: 10px; font-size:0.87em }}
p , li {{ text-align: justify; }}
h2 {{ text-align: center; margin: 0; }}
.date {{ text-align: right; }}
hr {{ border: #000 1px solid; }}
</style>
<h2>pyfa {0}</h2>
<div class="date"><small>{1}</small></div>
<hr>
{2}
{3}
"""


class UpdateDialog(wx.Dialog):
    def __init__(self, parent, release, version):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="pyfa Update Available", pos=wx.DefaultPosition,
                           size=wx.Size(550, 450), style=wx.DEFAULT_DIALOG_STYLE)

        self.UpdateSettings = svc_UpdateSettings.getInstance()
        self.releaseInfo = release
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        releaseDate = dateutil.parser.parse(self.releaseInfo['published_at'])
        notesSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browser = wx.html2.WebView.New(self)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.OnNewWindow)

        link_patterns = [
            (re.compile("([0-9a-f]{6,40})", re.I), r"https://github.com/pyfa-org/Pyfa/commit/\1"),
            (re.compile("#(\d+)", re.I), r"https://github.com/pyfa-org/Pyfa/issues/\1"),
            (re.compile("@(\w+)", re.I), r"https://github.com/\1")
        ]

        markdowner = markdown2.Markdown(
            extras=['cuddled-lists', 'fenced-code-blocks', 'target-blank-links', 'toc', 'link-patterns'],
            link_patterns=link_patterns)

        self.browser.SetPage(html_tmpl.format(
            self.releaseInfo['tag_name'],
            releaseDate.strftime('%B %d, %Y'),
            "<p class='text-danger'><b>This is a pre-release, be prepared for unstable features</b></p>" if version.is_prerelease else "",
            markdowner.convert(self.releaseInfo['body'])
        ), "")

        notesSizer.Add(self.browser, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        mainSizer.Add(notesSizer, 1, wx.EXPAND, 5)

        self.supressCheckbox = wx.CheckBox(self, wx.ID_ANY, "Don't remind me again for this release",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.supressCheckbox.Bind(wx.EVT_CHECKBOX, self.SuppressChange)

        mainSizer.Add(self.supressCheckbox, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0,
                      wx.EXPAND | wx.ALL, 5)

        actionSizer = wx.BoxSizer(wx.HORIZONTAL)

        goSizer = wx.BoxSizer(wx.VERTICAL)
        self.downloadButton = wx.Button(self, wx.ID_ANY, "Download", wx.DefaultPosition, wx.DefaultSize, 0)
        self.downloadButton.Bind(wx.EVT_BUTTON, self.OnDownload)
        goSizer.Add(self.downloadButton, 0, wx.ALL, 5)
        actionSizer.Add(goSizer, 1, wx.EXPAND, 5)

        self.closeButton = wx.Button(self, wx.ID_CLOSE)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        actionSizer.Add(self.closeButton, 0, wx.ALL, 5)
        mainSizer.Add(actionSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        # Handle use-case of suppressing a release, then a new version becoming available.
        # If that new version is not suppressed, the old version will remain in the preferences and
        # may cause confusion. If this dialog box is popping up for any reason, that mean we can
        # safely reset this setting
        self.UpdateSettings.set('version', None)

        self.Centre(wx.BOTH)

    def OnClose(self, e):
        self.Close()

    def OnNewWindow(self, event):
        url = event.GetURL()
        webbrowser.open(url)

    def SuppressChange(self, e):
        if self.supressCheckbox.IsChecked():
            self.UpdateSettings.set('version', self.releaseInfo['tag_name'])
        else:
            self.UpdateSettings.set('version', None)

    def OnDownload(self, e):
        wx.LaunchDefaultBrowser('https://github.com/pyfa-org/Pyfa/releases/tag/' + self.releaseInfo['tag_name'])
        self.OnClose(e)
