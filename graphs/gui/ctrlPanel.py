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
from gui.utils.inputs import FloatBox, FloatRangeBox
from service.const import GraphCacheCleanupReason
from service.fit import Fit
from .lists import SourceWrapperList, TargetWrapperList
from .vector import VectorPicker

InputData = namedtuple('InputData', ('handle', 'unit', 'value'))
InputBox = namedtuple('InputBox', ('handle', 'unit', 'textBox', 'icon', 'label'))
CheckBox = namedtuple('CheckBox', ('handle', 'checkBox'))
_t = wx.GetTranslation


class GraphControlPanel(wx.Panel):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame
        self._mainInputBox = None
        self._miscInputBoxes = []
        self._inputCheckboxes = []
        self._storedRanges = {}
        self._storedConsts = {}

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        optsSizer = wx.BoxSizer(wx.HORIZONTAL)

        commonOptsSizer = wx.BoxSizer(wx.VERTICAL)
        ySubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        yText = wx.StaticText(self, wx.ID_ANY, _t('Axis Y:'))
        ySubSelectionSizer.Add(yText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.ySubSelection = wx.Choice(self, wx.ID_ANY)
        self.ySubSelection.Bind(wx.EVT_CHOICE, self.OnYTypeUpdate)
        ySubSelectionSizer.Add(self.ySubSelection, 1, wx.EXPAND | wx.ALL, 0)
        commonOptsSizer.Add(ySubSelectionSizer, 0, wx.EXPAND | wx.ALL, 0)

        xSubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        xText = wx.StaticText(self, wx.ID_ANY, _t('Axis X:'))
        xSubSelectionSizer.Add(xText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.xSubSelection = wx.Choice(self, wx.ID_ANY)
        self.xSubSelection.Bind(wx.EVT_CHOICE, self.OnXTypeUpdate)
        xSubSelectionSizer.Add(self.xSubSelection, 1, wx.EXPAND | wx.ALL, 0)
        commonOptsSizer.Add(xSubSelectionSizer, 0, wx.EXPAND | wx.TOP, 5)

        self.showLegendCb = wx.CheckBox(self, wx.ID_ANY, _t('Show legend'), wx.DefaultPosition, wx.DefaultSize, 0)
        self.showLegendCb.SetValue(True)
        self.showLegendCb.Bind(wx.EVT_CHECKBOX, self.OnShowLegendChange)
        commonOptsSizer.Add(self.showLegendCb, 0, wx.EXPAND | wx.TOP, 5)
        self.showY0Cb = wx.CheckBox(self, wx.ID_ANY, _t('Always show Y = 0'), wx.DefaultPosition, wx.DefaultSize, 0)
        self.showY0Cb.SetValue(True)
        self.showY0Cb.Bind(wx.EVT_CHECKBOX, self.OnShowY0Change)
        commonOptsSizer.Add(self.showY0Cb, 0, wx.EXPAND | wx.TOP, 5)
        optsSizer.Add(commonOptsSizer, 0, wx.EXPAND | wx.RIGHT, 10)

        graphOptsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputsSizer = wx.BoxSizer(wx.VERTICAL)
        graphOptsSizer.Add(self.inputsSizer, 1, wx.EXPAND | wx.ALL, 0)

        vectorSize = 90 if 'wxGTK' in wx.PlatformInfo else 75
        self.srcVectorSizer = wx.BoxSizer(wx.VERTICAL)
        self.srcVectorLabel = wx.StaticText(self, wx.ID_ANY, '')
        self.srcVectorSizer.Add(self.srcVectorLabel, 0, wx.ALIGN_CENTER_HORIZONTAL| wx.BOTTOM, 5)
        self.srcVector = VectorPicker(self, style=wx.NO_BORDER, size=vectorSize, offset=0)
        self.srcVector.Bind(VectorPicker.EVT_VECTOR_CHANGED, self.OnNonMainInputChanged)
        self.srcVectorSizer.Add(self.srcVector, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        graphOptsSizer.Add(self.srcVectorSizer, 0, wx.EXPAND | wx.LEFT, 15)

        self.tgtVectorSizer = wx.BoxSizer(wx.VERTICAL)
        self.tgtVectorLabel = wx.StaticText(self, wx.ID_ANY, '')
        self.tgtVectorSizer.Add(self.tgtVectorLabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 5)
        self.tgtVector = VectorPicker(self, style=wx.NO_BORDER, size=vectorSize, offset=0)
        self.tgtVector.Bind(VectorPicker.EVT_VECTOR_CHANGED, self.OnNonMainInputChanged)
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

        self.srcTgtSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sourceList = SourceWrapperList(graphFrame, self)
        self.sourceList.SetMinSize((270, -1))
        self.srcTgtSizer.Add(self.sourceList, 1, wx.EXPAND | wx.ALL, 0)
        self.targetList = TargetWrapperList(graphFrame, self)
        self.targetList.SetMinSize((270, -1))
        self.srcTgtSizer.Add(self.targetList, 1, wx.EXPAND | wx.LEFT, 10)
        mainSizer.Add(self.srcTgtSizer, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)

        self.SetSizer(mainSizer)

        self.inputTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnInputTimer, self.inputTimer)
        self._setVectorDefaults()

    def updateControls(self, layout=True):
        if layout:
            self.Freeze()
        self._clearStoredValues()
        view = self.graphFrame.getView()

        self.refreshAxeLabels()

        # Vectors
        self._setVectorDefaults()
        if view.srcVectorDef is not None:
            self.srcVector.Show(True)
            self.srcVectorLabel.Show(True)
            self.srcVectorLabel.SetLabel(view.srcVectorDef.label)
        else:
            self.srcVector.Show(False)
            self.srcVectorLabel.Show(False)
        if view.tgtVectorDef is not None:
            self.tgtVector.Show(True)
            self.tgtVectorLabel.Show(True)
            self.tgtVectorLabel.SetLabel(view.tgtVectorDef.label)
        else:
            self.tgtVector.Show(False)
            self.tgtVectorLabel.Show(False)

        # Source and target list
        self.refreshColumns(layout=False)
        self.targetList.Show(view.hasTargets)

        # Inputs
        self._updateInputs(storeInputs=False)

        # Context icon
        self.contextIcon.Show(ContextMenu.hasMenu(self, None, None, (view.internalName,)))

        if layout:
            self.graphFrame.Layout()
            self.graphFrame.UpdateWindowSize()
            self.Thaw()

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
        for checkbox in self._inputCheckboxes:
            checkbox.checkBox.Destroy()
        self.inputsSizer.Clear()
        self._mainInputBox = None
        self._miscInputBoxes.clear()
        self._inputCheckboxes.clear()
        # Update vectors
        view = self.graphFrame.getView()
        handledHandles = set()
        if view.srcVectorDef is not None:
            self.__handleVector(view.srcVectorDef, self.srcVector, handledHandles, self.xType.mainInput[0])
        if view.tgtVectorDef is not None:
            self.__handleVector(view.tgtVectorDef, self.tgtVector, handledHandles, self.xType.mainInput[0])
        # Update inputs
        self.__addInputField(view.inputMap[self.xType.mainInput], handledHandles, mainInput=True)
        for inputDef in view.inputs:
            if inputDef.handle in handledHandles:
                continue
            self.__addInputField(inputDef, handledHandles)
        # Add checkboxes
        for checkboxDef in view.checkboxes:
            if checkboxDef.handle in handledHandles:
                continue
            self.__addInputCheckbox(checkboxDef, handledHandles)

    def __handleVector(self, vectorDef, vector, handledHandles, mainInputHandle):
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

    def __addInputField(self, inputDef, handledHandles, mainInput=False):
        if not self.__checkInputConditions(inputDef):
            return
        handledHandles.add(inputDef.handle)
        fieldSizer = wx.BoxSizer(wx.HORIZONTAL)
        tooltipText = (inputDef.mainTooltip if mainInput else inputDef.secondaryTooltip) or ''
        if mainInput:
            fieldTextBox = FloatRangeBox(self, self._storedRanges.get((inputDef.handle, inputDef.unit), inputDef.defaultRange))
            fieldTextBox.Bind(wx.EVT_TEXT, self.OnMainInputChanged)
        else:
            fieldTextBox = FloatBox(self, self._storedConsts.get((inputDef.handle, inputDef.unit), inputDef.defaultValue))
            fieldTextBox.Bind(wx.EVT_TEXT, self.OnNonMainInputChanged)
        fieldTextBox.SetToolTip(wx.ToolTip(tooltipText))
        fieldSizer.Add(fieldTextBox, 0, wx.EXPAND | wx.RIGHT, 5)
        fieldIcon = None
        if inputDef.iconID is not None:
            icon = BitmapLoader.getBitmap(inputDef.iconID, 'icons')
            if icon is not None:
                fieldIcon = wx.StaticBitmap(self)
                fieldIcon.SetBitmap(icon)
                fieldIcon.SetToolTip(wx.ToolTip(tooltipText))
                fieldSizer.Add(fieldIcon, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
        fieldLabel = wx.StaticText(self, wx.ID_ANY, self.formatLabel(inputDef))
        fieldLabel.SetToolTip(wx.ToolTip(tooltipText))
        fieldSizer.Add(fieldLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)
        self.inputsSizer.Add(fieldSizer, 0, wx.EXPAND | wx.BOTTOM, 5)
        # Store info about added input box
        inputBox = InputBox(handle=inputDef.handle, unit=inputDef.unit, textBox=fieldTextBox, icon=fieldIcon, label=fieldLabel)
        if mainInput:
            self._mainInputBox = inputBox
        else:
            self._miscInputBoxes.append(inputBox)

    def __addInputCheckbox(self, checkboxDef, handledHandles):
        if not self.__checkInputConditions(checkboxDef):
            return
        handledHandles.add(checkboxDef.handle)
        fieldCheckbox = wx.CheckBox(self, wx.ID_ANY, checkboxDef.label, wx.DefaultPosition, wx.DefaultSize, 0)
        fieldCheckbox.SetValue(self._storedConsts.get((checkboxDef.handle, None), checkboxDef.defaultValue))
        fieldCheckbox.Bind(wx.EVT_CHECKBOX, self.OnNonMainInputChanged)
        self.inputsSizer.Add(fieldCheckbox, 0, wx.BOTTOM, 5)
        # Store info about added checkbox
        checkbox = CheckBox(handle=checkboxDef.handle, checkBox=fieldCheckbox)
        self._inputCheckboxes.append(checkbox)

    def __checkInputConditions(self, inputDef):
        if not inputDef.conditions:
            return True
        selectedX = self.xType
        selectedY = self.yType
        for xCond, yCond in inputDef.conditions:
            xMatch = True
            yMatch = True
            if xCond is not None:
                xCondHandle, xCondUnit = xCond
                xMatch = selectedX.handle == xCondHandle and selectedX.unit == xCondUnit
            if yCond is not None:
                yCondHandle, yCondUnit = yCond
                yMatch = selectedY.handle == yCondHandle and selectedY.unit == yCondUnit
            if xMatch and yMatch:
                return True
        return False

    def refreshAxeLabels(self, restoreSelection=False):
        view = self.graphFrame.getView()
        if restoreSelection:
            selectedY = self.ySubSelection.GetSelection()
            selectedX = self.xSubSelection.GetSelection()
        else:
            selectedY = selectedX = 0

        self.ySubSelection.Clear()
        for yDef in view.yDefs:
            if yDef.hidden and not self.graphFrame.includeHidden:
                continue
            self.ySubSelection.Append(self.formatLabel(yDef, selector=True), yDef)
        self.ySubSelection.Enable(len(view.yDefs) > 1)
        self.ySubSelection.SetSelection(selectedY)

        self.xSubSelection.Clear()
        for xDef in view.xDefs:
            if xDef.hidden and not self.graphFrame.includeHidden:
                continue
            self.xSubSelection.Append(self.formatLabel(xDef, selector=True), xDef)
        self.xSubSelection.Enable(len(view.xDefs) > 1)
        self.xSubSelection.SetSelection(selectedX)

    def refreshColumns(self, layout=True):
        view = self.graphFrame.getView()
        self.sourceList.refreshExtraColumns(view.srcExtraCols)
        self.targetList.refreshExtraColumns(view.tgtExtraCols)
        self.srcTgtSizer.Detach(self.sourceList)
        self.srcTgtSizer.Detach(self.targetList)
        self.srcTgtSizer.Add(self.sourceList, self.sourceList.getWidthProportion(), wx.EXPAND | wx.ALL, 0)
        self.srcTgtSizer.Add(self.targetList, self.targetList.getWidthProportion(), wx.EXPAND | wx.LEFT, 10)
        self.Layout()

    def OnShowLegendChange(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnShowY0Change(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnYTypeUpdate(self, event):
        event.Skip()
        self._updateInputs()
        self.graphFrame.resetXMark()
        self.graphFrame.Layout()
        self.graphFrame.UpdateWindowSize()
        self.graphFrame.draw()

    def OnXTypeUpdate(self, event):
        event.Skip()
        self._updateInputs()
        self.graphFrame.resetXMark()
        self.graphFrame.Layout()
        self.graphFrame.UpdateWindowSize()
        self.graphFrame.draw()

    def OnMainInputChanged(self, event):
        event.Skip()
        self.graphFrame.resetXMark()
        self.inputTimer.Stop()
        self.inputTimer.Start(Fit.getInstance().serviceFittingOptions['marketSearchDelay'], True)

    def OnNonMainInputChanged(self, event):
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
        # Checkboxes
        for checkbox in self._inputCheckboxes:
            addMiscData(handle=checkbox.handle, unit=None, value=checkbox.checkBox.GetValue())

        return main, misc

    @property
    def showLegend(self):
        return self.showLegendCb.GetValue()

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
    def sources(self):
        return self.sourceList.wrappers

    @property
    def targets(self):
        return self.targetList.wrappers

    # Fit events
    def OnFitRenamed(self, event):
        self.sourceList.OnFitRenamed(event)
        self.targetList.OnFitRenamed(event)

    def OnFitChanged(self, event):
        self.sourceList.OnFitChanged(event)
        self.targetList.OnFitChanged(event)

    def OnFitRemoved(self, event):
        self.sourceList.OnFitRemoved(event)
        self.targetList.OnFitRemoved(event)

    # Target profile events
    def OnProfileRenamed(self, event):
        self.sourceList.OnProfileRenamed(event)
        self.targetList.OnProfileRenamed(event)

    def OnProfileChanged(self, event):
        self.sourceList.OnProfileChanged(event)
        self.targetList.OnProfileChanged(event)

    def OnProfileRemoved(self, event):
        self.sourceList.OnProfileRemoved(event)
        self.targetList.OnProfileRemoved(event)

    def OnResistModeChanged(self, event):
        self.targetList.OnResistModeChanged(event)

    def formatLabel(self, axisDef, selector=False):
        label = axisDef.selectorLabel if selector else axisDef.label
        if axisDef.unit is None:
            return label
        return '{}, {}'.format(label, axisDef.unit)

    def _storeCurrentValues(self):
        main, misc = self.getValues()
        if main is not None:
            self._storedRanges[(main.handle, main.unit)] = main.value
        for input in misc:
            self._storedConsts[(input.handle, input.unit)] = input.value

    def _clearStoredValues(self):
        self._storedRanges.clear()
        self._storedConsts.clear()

    def _setVectorDefaults(self):
        self.srcVector.SetValue(length=0, angle=90)
        self.tgtVector.SetValue(length=1, angle=90)

    def contextMenuHandler(self, event):
        viewName = self.graphFrame.getView().internalName
        menu = ContextMenu.getMenu(self, None, None, (viewName,))
        if menu is not None:
            self.PopupMenu(menu)
        event.Skip()
