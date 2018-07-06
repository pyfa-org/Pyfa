# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from .attributeSlider import AttributeSlider, EVT_VALUE_CHANGED

import gui.mainFrame
from gui.contextMenu import ContextMenu
from .itemAttributes import ItemParams
from gui.bitmap_loader import BitmapLoader
import gui.globalEvents as GE
import gui.mainFrame
import random

from logbook import Logger

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
            baseValueFormated = m.attribute.unit.TranslateValue(m.baseValue)[0]
            valueFormated = m.attribute.unit.TranslateValue(m.value)[0]
            slider = AttributeSlider(self, baseValueFormated, m.minMod, m.maxMod, not m.highIsGood)
            slider.SetValue(valueFormated, False)
            slider.Bind(EVT_VALUE_CHANGED, self.changeMutatedValue)
            self.event_mapping[slider] = m
            headingSizer = wx.BoxSizer(wx.HORIZONTAL)

            # create array for the two ranges
            min_t = [round(m.minValue, 3), m.minMod, None]
            max_t = [round(m.maxValue, 3), m.maxMod, None]

            # Then we need to determine if it's better than original, which will be the color
            min_t[2] = min_t[1] < 1 if not m.highIsGood else 1 < min_t[1]
            max_t[2] = max_t[1] < 1 if not m.highIsGood else 1 < max_t[1]

            # Lastly, we need to determine which range value is "worse" (left side) or "better" (right side)
            if (m.highIsGood and min_t[1] > max_t[1]) or (not m.highIsGood and min_t[1] < max_t[1]):
                better_range = min_t
            else:
                better_range = max_t

            if (m.highIsGood and max_t[1] < min_t[1]) or (not m.highIsGood and max_t[1] > min_t[1]):
                worse_range = max_t
            else:
                worse_range = min_t
            #
            # print("{}: \nHigh is good: {}".format(m.attribute.displayName, m.attribute.highIsGood))
            # print("Value {}".format(m.baseValue))
            #
            # print(min_t)
            # print(max_t)
            # print(better_range)
            # print(worse_range)

            font = parent.GetFont()
            font.SetWeight(wx.BOLD)

            headingSizer.Add(BitmapLoader.getStaticBitmap(m.attribute.iconID, self, "icons"), 0, wx.RIGHT, 10)

            displayName = wx.StaticText(self, wx.ID_ANY, m.attribute.displayName)
            displayName.SetFont(font)

            headingSizer.Add(displayName, 3, wx.ALL | wx.EXPAND, 0)


            range_low = wx.StaticText(self, wx.ID_ANY, ItemParams.FormatValue(*m.attribute.unit.TranslateValue(worse_range[0])))
            range_low.SetForegroundColour(self.goodColor if worse_range[2] else self.badColor)

            range_high = wx.StaticText(self, wx.ID_ANY, ItemParams.FormatValue(*m.attribute.unit.TranslateValue(better_range[0])))
            range_high.SetForegroundColour(self.goodColor if better_range[2] else self.badColor)

            headingSizer.Add(range_low, 0, wx.ALL | wx.EXPAND, 0)
            headingSizer.Add(wx.StaticText(self, wx.ID_ANY, " ─ "), 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
            headingSizer.Add(range_high, 0, wx.RIGHT | wx.EXPAND, 10)

            mainSizer.Add(headingSizer, 0, wx.ALL | wx.EXPAND, 5)

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
            value = m.attribute.unit.TranslateValue(value)[0]
            slider.SetValue(value)

        evt.Skip()

    def randomMutatedValues(self, evt):
        sFit = Fit.getInstance()

        for slider, m in self.event_mapping.items():
            value = random.uniform(m.minValue, m.maxValue)
            value = sFit.changeMutatedValue(m, value)
            value = m.attribute.unit.TranslateValue(value)[0]
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

