# noinspection PyPackageRequirements
import wx

from eos.saveddata.mode import Mode
from eos.saveddata.character import Skill
from eos.saveddata.implant import Implant
from eos.saveddata.booster import Booster
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from eos.saveddata.citadel import Citadel
from eos.saveddata.fit import Fit
from .attributeSlider import AttributeSlider

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.bitmap_loader import BitmapLoader


class ItemMutator(wx.Panel):

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.item = item

        self.activeFit = gui.mainFrame.MainFrame.getInstance().getActiveFit()
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.goodColor = wx.Colour(96, 191, 0)
        self.badColor = wx.Colour(255, 64, 0)

        for x in sorted(stuff.mutaplasmid.attributes, key=lambda a: a.displayName):
            # JFC this is ugly as sin
            min = round(x.min, 2)
            max = round(x.max, 2)

            value = stuff.itemModifiedAttributes.getOriginal(x.name)
            slider = AttributeSlider(self, value, min, max, not x.highIsGood)
            slider.SetValue(value)
            headingSizer = wx.BoxSizer(wx.HORIZONTAL)

            minValue = round(value * min, 3)
            maxValue = round(value * max, 3)

            # create array for the two ranges
            min_t = [minValue, min, None]
            max_t = [maxValue, max, None]

            # Then we need to determine if it's better than original, which will be the color
            min_t[2] = min_t[1] < 1 if not x.highIsGood else 1 < min_t[1]
            max_t[2] = max_t[1] < 1 if not x.highIsGood else 1 < max_t[1]

            # Lastly, we need to determine which range value is "worse" (left side) or "better" (right side)
            if (x.highIsGood and min_t[1] > max_t[1]) or (not x.highIsGood and min_t[1] < max_t[1]):
                better_range = min_t
            else:
                better_range = max_t

            if (x.highIsGood and max_t[1] < min_t[1]) or (not x.highIsGood and max_t[1] > min_t[1]):
                worse_range = max_t
            else:
                worse_range = min_t

            print("{}: \nHigh is good: {}".format(x.displayName, x.highIsGood))
            print("Value {}".format(value))

            print(min_t)
            print(max_t)
            print(better_range)
            print(worse_range)

            font = parent.GetFont()
            font.SetWeight(wx.BOLD)

            headingSizer.Add(BitmapLoader.getStaticBitmap(x.info.icon.iconFile, self, "icons"), 0, wx.RIGHT, 10)

            displayName = wx.StaticText(self, wx.ID_ANY, x.displayName)
            displayName.SetFont(font)

            headingSizer.Add(displayName, 3, wx.ALL | wx.EXPAND, 0)

            range_low = wx.StaticText(self, wx.ID_ANY, "{} {}".format(worse_range[0], x.unit.displayName))
            range_low.SetForegroundColour(self.goodColor if worse_range[2] else  self.badColor)

            range_high = wx.StaticText(self, wx.ID_ANY, "{} {}".format(better_range[0], x.unit.displayName))
            range_high.SetForegroundColour(self.goodColor if better_range[2] else self.badColor)

            headingSizer.Add(range_low, 0, wx.ALL | wx.EXPAND, 0)
            headingSizer.Add(wx.StaticText(self, wx.ID_ANY, " ── "), 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
            headingSizer.Add(range_high, 0, wx.RIGHT | wx.EXPAND, 10)

            mainSizer.Add(headingSizer, 0, wx.ALL | wx.EXPAND, 5)

            mainSizer.Add(slider, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)
            mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.AddStretchSpacer()

        self.m_staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline, 0, wx.EXPAND)

        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.saveBtn = wx.Button(self, wx.ID_ANY, "Save Attributes", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.saveBtn, 0, wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(bSizer, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 0)

        self.SetSizer(mainSizer)
        self.Layout()
