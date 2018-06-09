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

        for x in stuff.mutaplasmid.attributes:
            # JFC this is ugly as sin
            min = round(x.min, 2)
            max = round(x.max, 2)

            value = stuff.itemModifiedAttributes.getOriginal(x.name)
            slider = AttributeSlider(self, value, min, max, not x.highIsGood)
            slider.SetValue(value)
            headingSizer = wx.BoxSizer(wx.HORIZONTAL)

            minValue = round(value*min, 3)
            maxValue = round(value*max, 3)

            badValue = minValue if x.highIsGood else maxValue
            goodValue = maxValue if x.highIsGood else minValue
            print("{}: \nHigh is good: {}".format(x.displayName, x.highIsGood))

            minIsGood = badValue < value if not x.highIsGood else value < badValue
            maxIsGood = goodValue < value if not x.highIsGood else value < goodValue

            print ("======")
            print("Value {}".format(value))
            print("Min {} ({}) (good: {})".format(minValue, min, minIsGood))
            print("Max {} ({}) (good: {})".format(maxValue, max, maxIsGood))

            font = parent.GetFont()
            font.SetWeight(wx.BOLD)

            headingSizer.Add(BitmapLoader.getStaticBitmap(x.info.icon.iconFile, self, "icons"), 0, wx.RIGHT, 10)

            displayName = wx.StaticText(self, wx.ID_ANY, x.displayName)
            displayName.SetFont(font)

            headingSizer.Add(displayName, 3, wx.ALL | wx.EXPAND, 0)

            range_low = wx.StaticText(self, wx.ID_ANY, "{} {}".format(badValue, x.unit.displayName))
            range_low.SetForegroundColour(self.goodColor if minIsGood else self.badColor)

            range_high = wx.StaticText(self, wx.ID_ANY, "{} {}".format(goodValue, x.unit.displayName))
            range_high.SetForegroundColour(self.goodColor if maxIsGood else self.badColor)

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
