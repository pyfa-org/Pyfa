# noinspection PyPackageRequirements
import random

import wx
from logbook import Logger

import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from service.fit import Fit
from .attributeSlider import AttributeSlider, EVT_VALUE_CHANGED
from .itemAttributes import ItemParams

pyfalog = Logger(__name__)


class ItemMutator(wx.Panel):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.item = item
        self.timer = None
        self.activeFit = gui.mainFrame.MainFrame.getInstance().getActiveFit()
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.goodColor = wx.Colour(96, 191, 0)
        self.badColor = wx.Colour(255, 64, 0)

        self.event_mapping = {}

        for m in sorted(stuff.mutators.values(), key=lambda x: x.attribute.displayName):
            # Format: [raw value, modifier applied to base raw value, display value]
            range1 = (m.minValue, m.minMod, m.attribute.unit.SimplifyValue(m.minValue))
            range2 = (m.maxValue, m.maxMod, m.attribute.unit.SimplifyValue(m.maxValue))

            if (m.highIsGood and range1[0] >= range2[0]) or (not m.highIsGood and range1[0] <= range2[0]):
                betterRange = range1
                worseRange = range2
            else:
                betterRange = range2
                worseRange = range1

            if range1[2] >= range2[2]:
                displayMaxRange = range1
                displayMinRange = range2
            else:
                displayMaxRange = range2
                displayMinRange = range1

            headingSizer = wx.BoxSizer(wx.HORIZONTAL)

            font = parent.GetFont()
            font.SetWeight(wx.BOLD)

            headingSizer.Add(BitmapLoader.getStaticBitmap(m.attribute.iconID, self, "icons"), 0, wx.RIGHT, 10)

            displayName = wx.StaticText(self, wx.ID_ANY, m.attribute.displayName)
            displayName.SetFont(font)

            headingSizer.Add(displayName, 3, wx.ALL | wx.EXPAND, 0)

            leftVal = ItemParams.FormatValue(*m.attribute.unit.PreformatValue(displayMinRange[0]), rounding='dec')
            leftText = wx.StaticText(self, wx.ID_ANY, leftVal)
            leftText.SetForegroundColour(self.goodColor if displayMinRange is betterRange else self.badColor)

            rightVal = ItemParams.FormatValue(*m.attribute.unit.PreformatValue(displayMaxRange[0]), rounding='dec')
            rightText = wx.StaticText(self, wx.ID_ANY, rightVal)
            rightText.SetForegroundColour(self.goodColor if displayMaxRange is betterRange else self.badColor)

            headingSizer.Add(leftText, 0, wx.ALL | wx.EXPAND, 0)
            headingSizer.Add(wx.StaticText(self, wx.ID_ANY, " ─ "), 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
            headingSizer.Add(rightText, 0, wx.RIGHT | wx.EXPAND, 10)

            mainSizer.Add(headingSizer, 0, wx.ALL | wx.EXPAND, 5)

            slider = AttributeSlider(parent=self,
                                     baseValue=m.attribute.unit.SimplifyValue(m.baseValue),
                                     minValue=displayMinRange[2],
                                     maxValue=displayMaxRange[2],
                                     inverse=displayMaxRange is worseRange)
            slider.SetValue(m.attribute.unit.SimplifyValue(m.value), False)
            slider.Bind(EVT_VALUE_CHANGED, self.changeMutatedValue)
            self.event_mapping[slider] = m
            mainSizer.Add(slider, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

            mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.AddStretchSpacer()

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)

        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.refreshBtn = wx.Button(self, wx.ID_ANY, "Reset defaults", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.refreshBtn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.refreshBtn.Bind(wx.EVT_BUTTON, self.resetMutatedValues)

        self.randomBtn = wx.Button(self, wx.ID_ANY, "Random stats", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.randomBtn, 0, wx.ALIGN_CENTER_VERTICAL)
        self.randomBtn.Bind(wx.EVT_BUTTON, self.randomMutatedValues)

        mainSizer.Add(bSizer, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.Layout()

    def changeMutatedValue(self, evt):
        m = self.event_mapping[evt.Object]
        value = evt.Value
        value = m.attribute.unit.ComplicateValue(value)
        sFit = Fit.getInstance()

        sFit.changeMutatedValue(m, value)
        if self.timer:
            self.timer.Stop()
            self.timer = None

        for x in self.Parent.Children:
            if isinstance(x, ItemParams):
                x.RefreshValues(None)
                break
        self.timer = wx.CallLater(1000, self.callLater)

    def resetMutatedValues(self, evt):
        sFit = Fit.getInstance()

        for slider, m in self.event_mapping.items():
            value = sFit.changeMutatedValue(m, m.baseValue)
            value = m.attribute.unit.SimplifyValue(value)
            slider.SetValue(value)

        evt.Skip()

    def randomMutatedValues(self, evt):
        sFit = Fit.getInstance()

        for slider, m in self.event_mapping.items():
            value = random.uniform(m.minValue, m.maxValue)
            value = sFit.changeMutatedValue(m, value)
            value = m.attribute.unit.SimplifyValue(value)
            slider.SetValue(value)

        evt.Skip()

    def callLater(self):
        self.timer = None
        sFit = Fit.getInstance()

        # recalc the fit that this module affects. This is not necessarily the currently active fit
        sFit.refreshFit(self.activeFit)

        mainFrame = gui.mainFrame.MainFrame.getInstance()
        activeFit = mainFrame.getActiveFit()

        if activeFit != self.activeFit:
            # if we're no longer on the fit this module is affecting, simulate a "switch fit" so that the active fit
            # can be recalculated (if needed)
            sFit.switchFit(activeFit)

        # Send signal to GUI to update stats with current active fit
        wx.PostEvent(mainFrame, GE.FitChanged(fitID=activeFit))
