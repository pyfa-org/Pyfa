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
from gui.utils.inputs import FloatBox, FloatRangeBox, valToStr
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
        self._lastDynamicRange = None  # Track last applied dynamic range
        self._userModifiedMainInput = False  # Flag: has user manually changed main input?

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        optsSizer = wx.BoxSizer(wx.HORIZONTAL)

        commonOptsSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Row 1: Y axis
        ySubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        yText = wx.StaticText(self, wx.ID_ANY, _t('Axis Y:'))
        ySubSelectionSizer.Add(yText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.ySubSelection = wx.Choice(self, wx.ID_ANY)
        self.ySubSelection.Bind(wx.EVT_CHOICE, self.OnYTypeUpdate)
        ySubSelectionSizer.Add(self.ySubSelection, 1, wx.EXPAND, 0)
        commonOptsSizer.Add(ySubSelectionSizer, 0, wx.EXPAND, 0)

        # Row 2: X axis (hidden for segment graphs)
        self.xSubSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.xText = wx.StaticText(self, wx.ID_ANY, _t('Axis X:'))
        self.xSubSelectionSizer.Add(self.xText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.xSubSelection = wx.Choice(self, wx.ID_ANY)
        self.xSubSelection.Bind(wx.EVT_CHOICE, self.OnXTypeUpdate)
        self.xSubSelectionSizer.Add(self.xSubSelection, 1, wx.EXPAND, 0)
        commonOptsSizer.Add(self.xSubSelectionSizer, 0, wx.EXPAND | wx.TOP, 5)

        # Row 3: Color dropdown (only shown for graphs with segments) - Quality is in right column
        self.ammoStyleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ammoStyleText = wx.StaticText(self, wx.ID_ANY, _t('Style:'))
        self.ammoStyleSizer.Add(self.ammoStyleText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.ammoStyleSelection = wx.Choice(self, wx.ID_ANY)
        self.ammoStyleSelection.Append(_t('None'), 'none')
        self.ammoStyleSelection.Append(_t('Pattern'), 'pattern')
        self.ammoStyleSelection.Append(_t('Color'), 'color')
        self.ammoStyleSelection.SetSelection(2)  # Default to Color
        self.ammoStyleSelection.Bind(wx.EVT_CHOICE, self.OnAmmoStyleChange)
        self.ammoStyleSizer.Add(self.ammoStyleSelection, 1, wx.EXPAND, 0)
        commonOptsSizer.Add(self.ammoStyleSizer, 0, wx.EXPAND | wx.TOP, 5)

        # Row 4: Ammo Meta dropdown (moved from right column)
        self.ammoQualitySizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ammoQualityText = wx.StaticText(self, wx.ID_ANY, _t('Ammo Meta:'))
        self.ammoQualitySizer.Add(self.ammoQualityText, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.ammoQualitySelection = wx.Choice(self, wx.ID_ANY)
        self.ammoQualitySelection.Append(_t('T1'), 't1')
        self.ammoQualitySelection.Append(_t('Navy'), 'navy')
        self.ammoQualitySelection.Append(_t('All'), 'all')
        self.ammoQualitySelection.SetSelection(1)  # Default to Navy
        self.ammoQualitySelection.Bind(wx.EVT_CHOICE, self.OnAmmoQualityChange)
        self.ammoQualitySizer.Add(self.ammoQualitySelection, 1, wx.EXPAND, 0)
        commonOptsSizer.Add(self.ammoQualitySizer, 0, wx.EXPAND | wx.TOP, 5)

        # Row 5: Show legend checkbox
        self.showLegendCb = wx.CheckBox(self, wx.ID_ANY, _t('Show legend'), wx.DefaultPosition, wx.DefaultSize, 0)
        self.showLegendCb.SetValue(True)
        self.showLegendCb.Bind(wx.EVT_CHECKBOX, self.OnShowLegendChange)
        commonOptsSizer.Add(self.showLegendCb, 0, wx.TOP, 5)

        optsSizer.Add(commonOptsSizer, 0, wx.EXPAND | wx.RIGHT, 10)

        # Right column: inputs
        graphOptsSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Container for inputs (normal graphs)
        self.rightColumnSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Input fields sizer (shown for normal graphs) - at the top
        self.inputsSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightColumnSizer.Add(self.inputsSizer, 0, wx.EXPAND, 0)
        
        graphOptsSizer.Add(self.rightColumnSizer, 1, wx.EXPAND | wx.ALL, 0)

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

        # Ammo options and X axis visibility (only for graphs with segments)
        hasSegments = getattr(view, 'hasSegments', False)
        # Hide X axis dropdown for segment graphs (Application Profile)
        self.xText.Show(not hasSegments)
        self.xSubSelection.Show(not hasSegments)
        self.xSubSelectionSizer.ShowItems(not hasSegments)
        # Show ammo style (Color) dropdown for segment graphs (left column)
        self.ammoStyleText.Show(hasSegments)
        self.ammoStyleSelection.Show(hasSegments)
        self.ammoStyleSizer.ShowItems(hasSegments)
        # Show ammo quality dropdown for segment graphs (right column)
        self.ammoQualityText.Show(hasSegments)
        self.ammoQualitySelection.Show(hasSegments)
        self.ammoQualitySizer.ShowItems(hasSegments)
        
        # Check if we need to auto-switch ammo style when switching to/from segmented graphs
        if hasSegments:
            # First check if we should switch back to color (no conflicts)
            self.sourceList._checkAutoSwitchBackToColor()
            # Then check if we need to switch to pattern (conflicts exist)
            self.sourceList._checkAutoSwitchAmmoStyle()

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
            # Check if view has a dynamic default range method
            view = self.graphFrame.getView()
            defaultRange = inputDef.defaultRange
            if hasattr(view, 'getDefaultInputRange'):
                dynamicRange = view.getDefaultInputRange(inputDef, self.sources)
                if dynamicRange is not None:
                    defaultRange = dynamicRange
            fieldTextBox = FloatRangeBox(self, self._storedRanges.get((inputDef.handle, inputDef.unit), defaultRange))
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
        # Also refresh default columns for target list based on ammo style
        self.targetList.refreshDefaultColumns()
        self.srcTgtSizer.Detach(self.sourceList)
        self.srcTgtSizer.Detach(self.targetList)
        self.srcTgtSizer.Add(self.sourceList, self.sourceList.getWidthProportion(), wx.EXPAND | wx.ALL, 0)
        self.srcTgtSizer.Add(self.targetList, self.targetList.getWidthProportion(), wx.EXPAND | wx.LEFT, 10)
        self.Layout()

    def OnShowLegendChange(self, event):
        event.Skip()
        self.graphFrame.draw()

    def OnAmmoStyleChange(self, event):
        event.Skip()
        # Refresh target list columns to show/hide lightness/line style based on ammo style
        self.targetList.refreshDefaultColumns()
        self.graphFrame.draw()

    def OnAmmoQualityChange(self, event):
        event.Skip()
        # Clear cache when quality changes since we need to recalculate with different ammo
        self.graphFrame.clearCache(reason=GraphCacheCleanupReason.inputChanged)
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

    def _refreshMainInputRange(self):
        """
        Refresh the main input field's range based on current fit data.
        
        Called when fits change to update the distance range dynamically
        for graphs that support getDefaultInputRange (like Application Profile).
        """
        # If user has manually modified the main input, never override it
        if self._userModifiedMainInput:
            return
        
        if self._mainInputBox is None:
            return
        
        view = self.graphFrame.getView()
        if not hasattr(view, 'getDefaultInputRange'):
            return
        
        # Get the input definition for the main input
        mainInputKey = self.xType.mainInput
        if mainInputKey not in view.inputMap:
            return
        
        inputDef = view.inputMap[mainInputKey]
        
        # Check if user has manually modified the input field since last dynamic update
        currentRange = self._mainInputBox.textBox.GetValueRange()
        if currentRange:
            currentMin, currentMax = currentRange
            # Get the baseline to compare against
            if self._lastDynamicRange is not None:
                baselineMin, baselineMax = self._lastDynamicRange
            else:
                baselineMin, baselineMax = inputDef.defaultRange
            
            # If current range differs from the baseline, user has manually changed it
            # Set the flag permanently to prevent future overrides
            if currentMin != baselineMin or currentMax != baselineMax:
                self._userModifiedMainInput = True
                return
        
        # Calculate the new dynamic range
        dynamicRange = view.getDefaultInputRange(inputDef, self.sources)
        if dynamicRange is None:
            dynamicRange = inputDef.defaultRange
        
        # Store this as the last dynamic range we applied
        self._lastDynamicRange = dynamicRange
        
        # Clear the stored range so the new default is used
        storedKey = (inputDef.handle, inputDef.unit)
        if storedKey in self._storedRanges:
            del self._storedRanges[storedKey]
        
        # Update the text box with the new range
        self._mainInputBox.textBox.ChangeValue('{}-{}'.format(
            valToStr(dynamicRange[0]), valToStr(dynamicRange[1])))

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
    def ammoStyle(self):
        """Returns ammo style: 'none', 'pattern', or 'color'"""
        return self.ammoStyleSelection.GetClientData(self.ammoStyleSelection.GetSelection())

    def setAmmoStyle(self, style):
        """Set ammo style programmatically: 'none', 'pattern', or 'color'"""
        for i in range(self.ammoStyleSelection.GetCount()):
            if self.ammoStyleSelection.GetClientData(i) == style:
                self.ammoStyleSelection.SetSelection(i)
                # Trigger the same updates as OnAmmoStyleChange
                self.targetList.refreshDefaultColumns()
                self.graphFrame.draw()
                return

    @property
    def ammoQuality(self):
        """Returns ammo quality tier: 't1', 'navy', or 'all'"""
        return self.ammoQualitySelection.GetClientData(self.ammoQualitySelection.GetSelection())

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
        # Refresh the main input's default range when fit changes
        self._refreshMainInputRange()

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
