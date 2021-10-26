# noinspection PyPackageRequirements
import random

import wx
from logbook import Logger

import gui.fitCommands as cmd
import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from service.fit import Fit
from .attributeSlider import AttributeSlider, EVT_VALUE_CHANGED
from .itemAttributes import ItemParams


pyfalog = Logger(__name__)
_t = wx.GetTranslation

class ItemMutatorPanel(wx.Panel):

    def __init__(self, parent, stuff):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer.AddStretchSpacer()
        itemIcon = BitmapLoader.getStaticBitmap(stuff.item.iconID, self, "icons")
        if itemIcon is not None:
            headerSizer.Add(itemIcon, 0, 0, 0)
        mutaIcon = BitmapLoader.getStaticBitmap(stuff.mutaplasmid.item.iconID, self, "icons")
        if mutaIcon is not None:
            headerSizer.Add(mutaIcon, 0, wx.LEFT, 0)
        sourceItemText = wx.StaticText(self, wx.ID_ANY, stuff.fullName)
        font = parent.GetFont()
        font.SetWeight(wx.BOLD)
        sourceItemText.SetFont(font)
        headerSizer.Add(sourceItemText, 0, wx.LEFT, 10)
        headerSizer.AddStretchSpacer()
        mainSizer.Add(headerSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND, 0)

        self.mutaList = ItemMutatorList(self, stuff)
        mainSizer.Add(self.mutaList, 1, wx.EXPAND | wx.ALL, 0)

        mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.EXPAND, 0)
        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.refreshBtn = wx.Button(self, wx.ID_ANY, _t("Reset defaults"), wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.mutaList.resetMutatedValues)
        self.randomBtn = wx.Button(self, wx.ID_ANY, _t("Random stats"), wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.randomBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.randomBtn.Bind(wx.EVT_BUTTON, self.mutaList.randomMutatedValues)
        self.revertBtn = wx.Button(self, wx.ID_ANY, _t("Revert changes"), wx.DefaultPosition, wx.DefaultSize, 0)
        footerSizer.Add(self.revertBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.revertBtn.Bind(wx.EVT_BUTTON, self.mutaList.revertChanges)
        mainSizer.Add(footerSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

    def OnWindowClose(self):
        self.mutaList.OnWindowClose()


class ItemMutatorList(wx.ScrolledWindow):

    def __init__(self, parent, stuff):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(0, 15)
        self.carryingFitID = gui.mainFrame.MainFrame.getInstance().getActiveFit()
        self.initialMutations = {}
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.stuff = stuff
        self.timer = None
        self.isModified = False

        goodColor = wx.Colour(96, 191, 0)
        badColor = wx.Colour(255, 64, 0)
        font = parent.GetFont()
        font.SetWeight(wx.BOLD)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.event_mapping = {}
        higOverrides = {
            ('Stasis Web', 'speedFactor'): False,
            ('Damage Control', 'duration'): True,
            ('Siege Module', 'siegeLocalLogisticsDurationBonus'): False
        }
        first = True
        for m in sorted(stuff.mutators.values(), key=lambda x: x.attribute.displayName):
            if m.baseValue == 0:
                continue
            if not first:
                sizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)
            first = False

            self.initialMutations[m.attrID] = m.value

            highIsGood = higOverrides.get((stuff.item.group.name, m.attribute.name), m.highIsGood)
            # Format: [raw value, modifier applied to base raw value, display value]
            range1 = (m.minValue, self._simplifyValue(m, m.minValue))
            range2 = (m.maxValue, self._simplifyValue(m, m.maxValue))

            # minValue/maxValue do not always correspond to min/max, because these are
            # just base value multiplied by minMod/maxMod, and in case base is negative
            # minValue is actually bigger than maxValue
            if range1[0] <= range2[0]:
                minRange = range1
                maxRange = range2
            else:
                minRange = range2
                maxRange = range1

            if (highIsGood and minRange[0] >= maxRange[0]) or (not highIsGood and minRange[0] <= maxRange[0]):
                betterRange = minRange
                worseRange = maxRange
            else:
                betterRange = maxRange
                worseRange = minRange

            if minRange[1] >= maxRange[1]:
                displayMaxRange = minRange
                displayMinRange = maxRange
            else:
                displayMaxRange = maxRange
                displayMinRange = minRange

            # If base value is outside of mutation range, make sure that center of slider
            # corresponds to the value which is closest available to actual base value. It's
            # how EVE handles it
            if minRange[0] <= m.baseValue <= maxRange[0]:
                sliderBaseValue = m.baseValue
            else:
                sliderBaseValue = max(minRange[0], min(maxRange[0], m.baseValue))

            headingSizer = wx.BoxSizer(wx.HORIZONTAL)

            headingSizer.Add(BitmapLoader.getStaticBitmap(m.attribute.iconID, self, "icons"), 0, wx.RIGHT, 10)

            displayName = wx.StaticText(self, wx.ID_ANY, m.attribute.displayName)
            displayName.SetFont(font)

            headingSizer.Add(displayName, 3, wx.ALL | wx.EXPAND, 0)

            worseVal = ItemParams.FormatValue(*self._preformatValue(m, worseRange[0]), rounding='dec')
            worseText = wx.StaticText(self, wx.ID_ANY, worseVal)
            worseText.SetForegroundColour(badColor)

            betterVal = ItemParams.FormatValue(*self._preformatValue(m, betterRange[0]), rounding='dec')
            betterText = wx.StaticText(self, wx.ID_ANY, betterVal)
            betterText.SetForegroundColour(goodColor)

            headingSizer.Add(worseText, 0, wx.ALL | wx.EXPAND, 0)
            headingSizer.Add(wx.StaticText(self, wx.ID_ANY, " ─ "), 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
            headingSizer.Add(betterText, 0, wx.RIGHT | wx.EXPAND, 10)

            sizer.Add(headingSizer, 0, wx.ALL | wx.EXPAND, 5)

            slider = AttributeSlider(parent=self,
                                     baseValue=self._simplifyValue(m, sliderBaseValue),
                                     minValue=displayMinRange[1],
                                     maxValue=displayMaxRange[1],
                                     inverse=displayMaxRange is worseRange)
            slider.SetValue(self._simplifyValue(m, m.value), False)
            slider.Bind(EVT_VALUE_CHANGED, self.changeMutatedValue)
            self.event_mapping[slider] = m
            sizer.Add(slider, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

        self.SetSizer(sizer)

    def _simplifyValue(self, mutator, value):
        if mutator.attribute.unit is None:
            return value
        return mutator.attribute.unit.SimplifyValue(value)

    def _complicateValue(self, mutator, value):
        if mutator.attribute.unit is None:
            return value
        return mutator.attribute.unit.ComplicateValue(value)

    def _preformatValue(self, mutator, value):
        if mutator.attribute.unit is None:
            return value, None
        return mutator.attribute.unit.PreformatValue(value)

    def changeMutatedValue(self, evt):
        if evt.AffectsModifiedFlag:
            self.isModified = True
        m = self.event_mapping[evt.Object]
        value = evt.Value
        value = self._complicateValue(m, value)
        sFit = Fit.getInstance()

        sFit.changeMutatedValuePrelim(m, value)
        if self.timer:
            self.timer.Stop()
            self.timer = None

        for x in self.Parent.Parent.Children:
            if isinstance(x, ItemParams):
                x.RefreshValues(None)
                break
        self.timer = wx.CallLater(1000, self.callLater)

    def resetMutatedValues(self, evt):
        self.isModified = True
        sFit = Fit.getInstance()
        for slider, m in self.event_mapping.items():
            value = sFit.changeMutatedValuePrelim(m, m.baseValue)
            value = self._simplifyValue(m, value)
            slider.SetValue(value, affect_modified_flag=False)
        evt.Skip()

    def randomMutatedValues(self, evt):
        self.isModified = True
        sFit = Fit.getInstance()
        for slider, m in self.event_mapping.items():
            value = random.uniform(m.minValue, m.maxValue)
            value = sFit.changeMutatedValuePrelim(m, value)
            value = self._simplifyValue(m, value)
            slider.SetValue(value, affect_modified_flag=False)
        evt.Skip()

    def revertChanges(self, evt):
        self.isModified = False
        sFit = Fit.getInstance()
        for slider, m in self.event_mapping.items():
            if m.attrID in self.initialMutations:
                value = sFit.changeMutatedValuePrelim(m, self.initialMutations[m.attrID])
                value = self._simplifyValue(m, value)
                slider.SetValue(value, affect_modified_flag=False)
        evt.Skip()

    def OnWindowClose(self):
        # Submit mutation changes
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.carryingFitID)
        isCurrentMod = self.stuff in fit.modules
        isCurrentDrone = self.stuff in fit.drones
        if isCurrentMod or isCurrentDrone:
            if self.isModified:
                currentMutation = {}
                for slider, m in self.event_mapping.items():
                    # Sliders may have more up-to-date info than mutator in case we changed
                    # value in slider and without confirming it, decided to close window
                    value = slider.GetValue()
                    value = self._complicateValue(m, value)
                    if value != m.value:
                        value = sFit.changeMutatedValuePrelim(m, value)
                    currentMutation[m.attrID] = value
            else:
                currentMutation = self.initialMutations
            mainFrame = gui.mainFrame.MainFrame.getInstance()
            if isCurrentMod:
                mainFrame.getCommandForFit(self.carryingFitID).Submit(cmd.GuiChangeLocalModuleMutationCommand(
                    fitID=self.carryingFitID,
                    position=fit.modules.index(self.stuff),
                    mutation=currentMutation,
                    oldMutation=self.initialMutations))
            elif isCurrentDrone:
                mainFrame.getCommandForFit(self.carryingFitID).Submit(cmd.GuiChangeLocalDroneMutationCommand(
                    fitID=self.carryingFitID,
                    position=fit.drones.index(self.stuff),
                    mutation=currentMutation,
                    oldMutation=self.initialMutations))
        for slider in self.event_mapping:
            slider.OnWindowClose()

    def callLater(self):
        self.timer = None
        sFit = Fit.getInstance()

        # recalc the fit that this module affects. This is not necessarily the currently active fit
        sFit.refreshFit(self.carryingFitID)

        mainFrame = gui.mainFrame.MainFrame.getInstance()
        activeFit = mainFrame.getActiveFit()

        if activeFit != self.carryingFitID:
            # if we're no longer on the fit this module is affecting, simulate a "switch fit" so that the active fit
            # can be recalculated (if needed)
            sFit.switchFit(activeFit)

        # Send signal to GUI to update stats with current active fit
        wx.PostEvent(mainFrame, GE.FitChanged(fitIDs=(activeFit,)))
