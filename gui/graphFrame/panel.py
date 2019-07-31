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


from collections import namedtuple

# noinspection PyPackageRequirements
import wx

from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenu
from service.const import GraphCacheCleanupReason
from service.fit import Fit
from gui.utils.inputs import FloatBox, FloatRangeBox
from .lists import FitList, TargetList
from .vector import VectorPicker


InputData = namedtuple('InputData', ('handle', 'unit', 'value'))
InputBox = namedtuple('InputBox', ('handle', 'unit', 'textBox', 'icon', 'label'))


class GraphControlPanel(wx.Panel):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame
        self._mainInputBox = None
        self._miscInputBoxes = []
        self._storedRanges = {}
        self._storedConsts = {}

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        optsSizer = wx.BoxSizer(wx.HORIZONTAL)

        commonOptsSizer = wx.BoxSizer(wx.VERTICAL)
        ySubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        yText = wx.StaticText(self, wx.ID_ANY, 'Axis Y:')
        ySubSelectionSizer.Add(yText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.ySubSelection = wx.Choice(self, wx.ID_ANY)
        self.ySubSelection.Bind(wx.EVT_CHOICE, self.OnYTypeUpdate)
        ySubSelectionSizer.Add(self.ySubSelection, 1, wx.EXPAND | wx.ALL, 0)
        commonOptsSizer.Add(ySubSelectionSizer, 0, wx.EXPAND | wx.ALL, 0)

        xSubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        xText = wx.StaticText(self, wx.ID_ANY, 'Axis X:')
        xSubSelectionSizer.Add(xText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.xSubSelection = wx.Choice(self, wx.ID_ANY)
        self.xSubSelection.Bind(wx.EVT_CHOICE, self.OnXTypeUpdate)
        xSubSelectionSizer.Add(self.xSubSelection, 1, wx.EXPAND | wx.ALL, 0)
        commonOptsSizer.Add(xSubSelectionSizer, 0, wx.EXPAND | wx.TOP, 5)

        self.showY0Cb = wx.CheckBox(self, wx.ID_ANY, 'Always show Y = 0', wx.DefaultPosition, wx.DefaultSize, 0)
        self.showY0Cb.SetValue(True)
        self.showY0Cb.Bind(wx.EVT_CHECKBOX, self.OnShowY0Change)
        commonOptsSizer.Add(self.showY0Cb, 0, wx.EXPAND | wx.TOP, 5)
        optsSizer.Add(commonOptsSizer, 0, wx.EXPAND | wx.RIGHT, 10)

        graphOptsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputsSizer = wx.BoxSizer(wx.VERTICAL)
        graphOptsSizer.Add(self.inputsSizer, 1, wx.EXPAND | wx.ALL, 0)

        self.srcVectorSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcVectorLabel = wx.StaticText(self, wx.ID_ANY, '')
        self.srcVectorSizer.Add(self.srcVectorLabel, 0, wx.ALIGN_CENTER_HORIZONTAL| wx.BOTTOM, 5)
        self.srcVector = VectorPicker(self, style=wx.NO_BORDER, size=75, offset=0)
        self.srcVector.Bind(VectorPicker.EVT_VECTOR_CHANGED, self.OnFieldChanged)
        self.srcVectorSizer.Add(self.srcVector, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        graphOptsSizer.Add(self.srcVectorSizer, 0, wx.EXPAND | wx.LEFT, 15)

        self.tgtVectorSizer = wx.BoxSizer(wx.VERTICAL)
        self.tgtVectorLabel = wx.StaticText(self, wx.ID_ANY, '')
        self.tgtVectorSizer.Add(self.tgtVectorLabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 5)
        self.tgtVector = VectorPicker(self, style=wx.NO_BORDER, size=75, offset=0)
        self.tgtVector.Bind(VectorPicker.EVT_VECTOR_CHANGED, self.OnFieldChanged)
        self.tgtVectorSizer.Add(self.tgtVector, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        graphOptsSizer.Add(self.tgtVectorSizer, 0, wx.EXPAND | wx.LEFT, 10)

        optsSizer.Add(graphOptsSizer, 1, wx.EXPAND | wx.ALL, 0)

        contextSizer = wx.BoxSizer(wx.VERTICAL)
        savedFont = self.GetFont()
        contextIconFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        contextIconFont.SetPointSize(8)
        self.SetFont(contextIconFont)
        self.contextIcon = wx.StaticText(self, wx.ID_ANY, '\u2630', size=wx.Size((10, -1)))
        self.contextIcon.Bind(wx.EVT_CONTEXT_MENU, self.contextMenuHandler)
        self.contextIcon.Bind(wx.EVT_LEFT_UP, self.contextMenuHandler)
        self.SetFont(savedFont)
        contextSizer.Add(self.contextIcon, 0, wx.EXPAND | wx.ALL, 0)
        optsSizer.Add(contextSizer, 0, wx.EXPAND | wx.ALL, 0)

        mainSizer.Add(optsSizer, 0, wx.EXPAND | wx.ALL, 10)

        srcTgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fitList = FitList(graphFrame, self)
        self.fitList.SetMinSize((270, -1))
        srcTgtSizer.Add(self.fitList, 1, wx.EXPAND | wx.ALL, 0)
        self.targetList = TargetList(graphFrame, self)
        self.targetList.SetMinSize((270, -1))
        srcTgtSizer.Add(self.targetList, 1, wx.EXPAND | wx.LEFT, 10)
        mainSizer.Add(srcTgtSizer, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

        self.SetSizer(mainSizer)

        self.inputTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnInputTimer, self.inputTimer)
        self._setVectorDefaults()

    def updateControls(self, layout=True):
        self._clearStoredValues()
        view = self.graphFrame.getView()
        self.ySubSelection.Clear()
        self.xSubSelection.Clear()
        for yDef in view.yDefs:
            self.ySubSelection.Append(self.formatLabel(yDef), yDef)
        self.ySubSelection.SetSelection(0)
        self.ySubSelection.Enable(len(view.yDefs) > 1)
        for xDef in view.xDefs:
            self.xSubSelection.Append(self.formatLabel(xDef), xDef)
        self.xSubSelection.SetSelection(0)
        self.xSubSelection.Enable(len(view.xDefs) > 1)

        # Vectors
        self._setVectorDefaults()
        if view.srcVectorDef is not None:
            self.srcVectorLabel.SetLabel(view.srcVectorDef.label)
            self.srcVector.Show(True)
            self.srcVectorLabel.Show(True)
        else:
            self.srcVector.Show(False)
            self.srcVectorLabel.Show(False)
        if view.tgtVectorDef is not None:
            self.tgtVectorLabel.SetLabel(view.tgtVectorDef.label)
            self.tgtVector.Show(True)
            self.tgtVectorLabel.Show(True)
        else:
            self.tgtVector.Show(False)
            self.tgtVectorLabel.Show(False)

        # Source and target list
        self.fitList.refreshExtraColumns(view.srcExtraCols)
        self.targetList.refreshExtraColumns(view.tgtExtraCols)
        self.targetList.Show(view.hasTargets)

        # Inputs
        self._updateInputs(storeInputs=False)

        # Context icon
        self.contextIcon.Show(ContextMenu.hasMenu(self, None, None, (view.internalName,)))

        if layout:
            self.graphFrame.Layout()
            self.graphFrame.UpdateWindowSize()

    def _updateInputs(self, storeInputs=True):
        if storeInputs:
            self._storeCurrentValues()
        # Clean up old inputs
        for inputBox in (self._mainInputBox, *self._miscInputBoxes):
            if inputBox is None:
                continue
            for child in (inputBox.textBox, inputBox.icon, inputBox.label):
                if child is not None:
                    child.Destroy()
        self.inputsSizer.Clear()
        self._mainInputBox = None
        self._miscInputBoxes.clear()

        # Update vectors
        def handleVector(vectorDef, vector, handledHandles, mainInputHandle):
            handledHandles.add(vectorDef.lengthHandle)
            handledHandles.add(vectorDef.angleHandle)
            try:
                storedLength = self._storedConsts[(vectorDef.lengthHandle, vectorDef.lengthUnit)]
            except KeyError:
                pass
            else:
                vector.SetLength(storedLength / 100)
            try:
                storedAngle = self._storedConsts[(vectorDef.angleHandle, vectorDef.angleUnit)]
            except KeyError:
                pass
            else:
                vector.SetAngle(storedAngle)
            vector.SetDirectionOnly(vectorDef.lengthHandle == mainInputHandle)

        view = self.graphFrame.getView()
        handledHandles = set()
        if view.srcVectorDef is not None:
            handleVector(view.srcVectorDef, self.srcVector, handledHandles, self.xType.mainInput[0])
        if view.tgtVectorDef is not None:
            handleVector(view.tgtVectorDef, self.tgtVector, handledHandles, self.xType.mainInput[0])

        # Update inputs
        def addInputField(inputDef, handledHandles, mainInput=False):
            handledHandles.add(inputDef.handle)
            fieldSizer = wx.BoxSizer(wx.HORIZONTAL)
            if mainInput:
                fieldTextBox = FloatRangeBox(self, self._storedRanges.get((inputDef.handle, inputDef.unit), inputDef.defaultRange))
            else:
                fieldTextBox = FloatBox(self, self._storedConsts.get((inputDef.handle, inputDef.unit), inputDef.defaultValue))
            fieldTextBox.Bind(wx.EVT_TEXT, self.OnFieldChanged)
            fieldSizer.Add(fieldTextBox, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
            fieldIcon = None
            if inputDef.iconID is not None:
                icon = BitmapLoader.getBitmap(inputDef.iconID, 'icons')
                if icon is not None:
                    fieldIcon = wx.StaticBitmap(self)
                    fieldIcon.SetBitmap(icon)
                    fieldSizer.Add(fieldIcon, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
            fieldLabel = wx.StaticText(self, wx.ID_ANY, self.formatLabel(inputDef))
            fieldSizer.Add(fieldLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
            self.inputsSizer.Add(fieldSizer, 0, wx.EXPAND | wx.BOTTOM, 5)
            # Store info about added input box
            inputBox = InputBox(handle=inputDef.handle, unit=inputDef.unit, textBox=fieldTextBox, icon=fieldIcon, label=fieldLabel)
            if mainInput:
                self._mainInputBox = inputBox
            else:
                self._miscInputBoxes.append(inputBox)


        addInputField(view.inputMap[self.xType.mainInput], handledHandles, mainInput=True)
        for inputDef in view.inputs:
            if inputDef.mainOnly:
                continue
            if inputDef.handle in handledHandles:
                continue
            addInputField(inputDef, handledHandles)

    def OnShowY0Change(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnYTypeUpdate(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnXTypeUpdate(self, event):
        event.Skip()
        self._updateInputs()
        self.graphFrame.Layout()
        self.graphFrame.UpdateWindowSize()
        self.graphFrame.draw()

    def OnFieldChanged(self, event):
        event.Skip()
        self.inputTimer.Stop()
        self.inputTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def OnInputTimer(self, event):
        event.Skip()
        self.graphFrame.clearCache(reason=GraphCacheCleanupReason.inputChanged)
        self.graphFrame.draw()

    def getValues(self):
        view = self.graphFrame.getView()
        misc = []
        processedHandles = set()

        def addMiscData(handle, unit, value):
            if handle in processedHandles:
                return
            inputData = InputData(handle=handle, unit=unit, value=value)
            misc.append(inputData)

        # Main input box
        main = InputData(handle=self._mainInputBox.handle, unit=self._mainInputBox.unit, value=self._mainInputBox.textBox.GetValueRange())
        processedHandles.add(self._mainInputBox.handle)
        # Vectors
        srcVectorDef = view.srcVectorDef
        if srcVectorDef is not None:
            if not self.srcVector.IsDirectionOnly:
                addMiscData(handle=srcVectorDef.lengthHandle, unit=srcVectorDef.lengthUnit, value=self.srcVector.GetLength() * 100)
            addMiscData(handle=srcVectorDef.angleHandle, unit=srcVectorDef.angleUnit, value=self.srcVector.GetAngle())
        tgtVectorDef = view.tgtVectorDef
        if tgtVectorDef is not None:
            if not self.tgtVector.IsDirectionOnly:
                addMiscData(handle=tgtVectorDef.lengthHandle, unit=tgtVectorDef.lengthUnit, value=self.tgtVector.GetLength() * 100)
            addMiscData(handle=tgtVectorDef.angleHandle, unit=tgtVectorDef.angleUnit, value=self.tgtVector.GetAngle())
        # Other input boxes
        for inputBox in self._miscInputBoxes:
            addMiscData(handle=inputBox.handle, unit=inputBox.unit, value=inputBox.textBox.GetValueFloat())

        return main, misc

    @property
    def showY0(self):
        return self.showY0Cb.GetValue()

    @property
    def yType(self):
        return self.ySubSelection.GetClientData(self.ySubSelection.GetSelection())

    @property
    def xType(self):
        return self.xSubSelection.GetClientData(self.xSubSelection.GetSelection())

    @property
    def fits(self):
        return self.fitList.fits

    @property
    def targets(self):
        return self.targetList.targets

    # Fit events
    def OnFitRenamed(self, event):
        self.fitList.OnFitRenamed(event)
        self.targetList.OnFitRenamed(event)

    def OnFitChanged(self, event):
        self.fitList.OnFitChanged(event)
        self.targetList.OnFitChanged(event)

    def OnFitRemoved(self, event):
        self.fitList.OnFitRemoved(event)
        self.targetList.OnFitRemoved(event)

    # Target profile events
    def OnProfileRenamed(self, event):
        self.targetList.OnProfileRenamed(event)

    def OnProfileChanged(self, event):
        self.targetList.OnProfileChanged(event)

    def OnProfileRemoved(self, event):
        self.targetList.OnProfileRemoved(event)

    def formatLabel(self, axisDef):
        if axisDef.unit is None:
            return axisDef.label
        return '{}, {}'.format(axisDef.label, axisDef.unit)

    def _storeCurrentValues(self):
        main, misc = self.getValues()
        if main is not None:
            self._storedRanges[(main.handle, main.unit)] = main.value
        for input in misc:
            self._storedConsts[(input.handle, input.unit)] = input.value

    def _clearStoredValues(self):
        self._storedConsts.clear()
        self._storedRanges.clear()

    def _setVectorDefaults(self):
        self.srcVector.SetValue(length=0, angle=90)
        self.tgtVector.SetValue(length=1, angle=90)

    def contextMenuHandler(self, event):
        viewName = self.graphFrame.getView().internalName
        menu = ContextMenu.getMenu(self, None, None, (viewName,))
        if menu is not None:
            self.PopupMenu(menu)
        event.Skip()
