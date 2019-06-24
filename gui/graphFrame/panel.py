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

from gui.bitmap_loader import BitmapLoader
from service.fit import Fit
from .lists import FitList, TargetList
from .vector import VectorPicker, DirectionPicker


class GraphControlPanel(wx.Panel):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame

        self.fields = {}

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        paramSizer = wx.BoxSizer(wx.HORIZONTAL)
        viewOptSizer = wx.BoxSizer(wx.VERTICAL)
        self.showY0Cb = wx.CheckBox(self, wx.ID_ANY, 'Always show Y = 0', wx.DefaultPosition, wx.DefaultSize, 0)
        self.showY0Cb.SetValue(True)
        self.showY0Cb.Bind(wx.EVT_CHECKBOX, self.OnShowY0Change)
        viewOptSizer.Add(self.showY0Cb, 0, wx.LEFT | wx.TOP | wx.RIGHT | wx.EXPAND, 5)
        self.graphSubselSizer = wx.BoxSizer(wx.VERTICAL)
        viewOptSizer.Add(self.graphSubselSizer, 0, wx.ALL | wx.EXPAND, 5)
        paramSizer.Add(viewOptSizer, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        self.inputsSizer = wx.FlexGridSizer(0, 4, 0, 0)
        self.inputsSizer.AddGrowableCol(1)
        paramSizer.Add(self.inputsSizer, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        mainSizer.Add(paramSizer, 0, wx.EXPAND | wx.ALL, 0)

        srcTgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fitList = FitList(graphFrame, self)
        self.fitList.SetMinSize((270, -1))
        srcTgtSizer.Add(self.fitList, 1, wx.EXPAND)
        self.srcVector = VectorPicker(self, style=wx.NO_BORDER, size=60, offset=90, label='Src', labelpos=2)
        srcTgtSizer.Add(self.srcVector, flag=wx.SHAPED | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.tgtVector = DirectionPicker(self, style=wx.NO_BORDER, size=60, offset=-90, label='Tgt', labelpos=3)
        srcTgtSizer.Add(self.tgtVector, flag=wx.SHAPED | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.targets = []
        self.targetList = TargetList(graphFrame, self)
        self.targetList.SetMinSize((270, -1))
        self.targetList.update(self.targets)
        srcTgtSizer.Add(self.targetList, 1, wx.EXPAND)
        mainSizer.Add(srcTgtSizer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(mainSizer)

        self.drawTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnDrawTimer, self.drawTimer)

    def getValues(self):
        values = {}
        for fieldHandle, field in self.fields.items():
            values[fieldHandle] = field.GetValue()
        return values

    @property
    def showY0(self):
        return self.showY0Cb.GetValue()

    def updateControlsForView(self, view):
        self.graphSubselSizer.Clear()
        self.inputsSizer.Clear()
        for child in self.Children:
            if child not in (self.showY0Cb, self.fitList, self.targetList, self.srcVector, self.tgtVector):
                child.Destroy()
        self.fields.clear()


        def formatAxisLabel(axisDef):
            if axisDef.unit is None:
                return axisDef.label
            return '{}, {}'.format(axisDef.label, axisDef.unit)

        selectedXRb = wx.RadioBox(self, -1, 'Axis X', wx.DefaultPosition, wx.DefaultSize, [formatAxisLabel(x) for x in view.xDefs], 1, wx.RA_SPECIFY_COLS)
        self.graphSubselSizer.Add(selectedXRb, 0, wx.ALL | wx.EXPAND, 0)
        selectedYRb = wx.RadioBox(self, -1, 'Axis Y', wx.DefaultPosition, wx.DefaultSize, [formatAxisLabel(y) for y in view.yDefs], 1, wx.RA_SPECIFY_COLS)
        self.graphSubselSizer.Add(selectedYRb, 0, wx.ALL | wx.EXPAND, 0)

        # Setup inputs
        shownHandles = set()
        if view.hasSrcVector:
            shownHandles.add(view.srcVectorLengthHandle)
            shownHandles.add(view.srcVectorAngleHandle)
        if view.hasTgtVector:
            shownHandles.add(view.tgtVectorLengthHandle)
            shownHandles.add(view.tgtVectorAngleHandle)
        for inputHandle in (view.xDefs[0].mainInputHandle, *(i.handle for i in view.inputs)):
            if inputHandle in shownHandles:
                continue
            shownHandles.add(inputHandle)
            inputDef = view.inputMap[inputHandle]
            textBox = wx.TextCtrl(self, wx.ID_ANY, style=0)
            textBox.Bind(wx.EVT_TEXT, self.OnFieldChanged)
            self.inputsSizer.Add(textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            if inputDef.defaultValue is not None:
                inputDefault = inputDef.defaultValue
                if not isinstance(inputDefault, str):
                    inputDefault = ('%f' % inputDefault).rstrip('0')
                    if inputDefault[-1:] == '.':
                        inputDefault += '0'
                textBox.ChangeValue(inputDefault)
            imgLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
            if inputDef.iconID is not None:
                icon = BitmapLoader.getBitmap(inputDef.iconID, 'icons')
                if icon is not None:
                    static = wx.StaticBitmap(self)
                    static.SetBitmap(icon)
                    imgLabelSizer.Add(static, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)

            imgLabelSizer.Add(wx.StaticText(self, wx.ID_ANY, inputDef.label), 0,
                              wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
            self.inputsSizer.Add(imgLabelSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.Layout()

    def OnShowY0Change(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnYTypeUpdate(self, event):
        event.Skip()
        obj = event.GetEventObject()
        formatName = obj.GetLabel()
        self.graphFrame.draw()

    def OnFieldChanged(self, event):
        event.Skip()
        self.drawTimer.Stop()
        self.drawTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def OnDrawTimer(self, event):
        event.Skip()
        self.graphFrame.clearCache()
        self.graphFrame.draw()

    def unbindExternalEvents(self):
        self.fitList.unbindExternalEvents()

