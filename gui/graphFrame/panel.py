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

from service.fit import Fit
from .lists import FitList, TargetList


class GraphControlPanel(wx.Panel):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame

        self.selectedY = None
        self.selectedYRbMap = {}

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        paramSizer = wx.BoxSizer(wx.HORIZONTAL)
        viewOptSizer = wx.BoxSizer(wx.VERTICAL)
        self.showY0Cb = wx.CheckBox(self, wx.ID_ANY, 'Always show Y = 0', wx.DefaultPosition, wx.DefaultSize, 0)
        self.showY0Cb.SetValue(True)
        viewOptSizer.Add(self.showY0Cb, 0, wx.LEFT | wx.TOP | wx.RIGHT | wx.EXPAND, 5)
        self.graphSubselSizer = wx.BoxSizer(wx.VERTICAL)
        viewOptSizer.Add(self.graphSubselSizer, 0, wx.ALL | wx.EXPAND, 5)
        paramSizer.Add(viewOptSizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        self.inputsSizer = wx.FlexGridSizer(0, 4, 0, 0)
        self.inputsSizer.AddGrowableCol(1)
        paramSizer.Add(self.inputsSizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        mainSizer.Add(paramSizer, 0, wx.EXPAND | wx.ALL, 0)

        srcTgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        fit = Fit.getInstance().getFit(self.graphFrame.mainFrame.getActiveFit())
        self.fits = [fit] if fit is not None else []
        self.fitList = FitList(self)
        self.fitList.SetMinSize((270, -1))
        self.fitList.fitList.update(self.fits)
        srcTgtSizer.Add(self.fitList, 1, wx.EXPAND)
        self.targets = []
        self.targetList = TargetList(self)
        self.targetList.SetMinSize((270, -1))
        self.targetList.targetList.update(self.targets)
        srcTgtSizer.Add(self.targetList, 1, wx.EXPAND)
        mainSizer.Add(srcTgtSizer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(mainSizer)

    @property
    def showY0(self):
        return self.showY0Cb.GetValue()

