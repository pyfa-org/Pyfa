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
from gui.preferenceView import PreferenceView


class DummyView(PreferenceView):
    title = "Dummy"

    def populatePanel(self, panel):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        headerSizer = self.initHeader(panel)
        mainSizer.Add(headerSizer, 0, wx.EXPAND, 5)

        self.stline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.stline1, 0, wx.EXPAND, 5)

        contentSizer = self.initContent(panel)
        mainSizer.Add(contentSizer, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 10)

        self.stline2 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.stline2, 0, wx.EXPAND, 5)

        footerSizer = self.initFooter(panel)
        mainSizer.Add(footerSizer, 0, wx.EXPAND, 5)
        panel.SetSizer(mainSizer)
        panel.Layout()

    def refreshPanel(self, fit):
        pass

    def initHeader(self, panel):
        headerSizer = wx.BoxSizer(wx.VERTICAL)
        self.stTitle = wx.StaticText(panel, wx.ID_ANY, "Dummy", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(14, 70, 90, 90, False, wx.EmptyString))
        headerSizer.Add(self.stTitle, 0, wx.ALL, 5)

        return headerSizer

    def initContent(self, panel):
        contentSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_checkBox2 = wx.CheckBox(panel, wx.ID_ANY, "Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        contentSizer.Add(self.m_checkBox2, 0, wx.ALL, 5)

        self.m_radioBtn2 = wx.RadioButton(panel, wx.ID_ANY, "RadioBtn", wx.DefaultPosition, wx.DefaultSize, 0)
        contentSizer.Add(self.m_radioBtn2, 0, wx.ALL, 5)

        self.m_slider2 = wx.Slider(panel, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        contentSizer.Add(self.m_slider2, 0, wx.ALL, 5)

        self.m_gauge1 = wx.Gauge(panel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        contentSizer.Add(self.m_gauge1, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        contentSizer.Add(self.m_textCtrl2, 0, wx.ALL, 5)

        return contentSizer

    def initFooter(self, panel):
        footerSizer = wx.BoxSizer(wx.HORIZONTAL)

        footerSizer.AddStretchSpacer()
        self.btnRestore = wx.Button(panel, wx.ID_ANY, "Restore", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnRestore.Enable(False)

        footerSizer.Add(self.btnRestore, 0, wx.ALL, 5)

        self.btnApply = wx.Button(panel, wx.ID_ANY, "Apply", wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.btnApply, 0, wx.ALL, 5)
        return footerSizer


DummyView.register()
