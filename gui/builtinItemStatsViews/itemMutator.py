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
    ORDER = [Fit, Ship, Citadel, Mode, Module, Drone, Fighter, Implant, Booster, Skill]

    def __init__(self, parent, stuff, item):
        wx.Panel.__init__(self, parent)
        self.stuff = stuff
        self.item = item

        self.activeFit = gui.mainFrame.MainFrame.getInstance().getActiveFit()
        mainSizer = wx.BoxSizer(wx.VERTICAL)


        for x in stuff.mutaplasmid.attributes:
            # convert to percentages
            min = round(x.min, 2)
            max = round(x.max, 2)
            value = stuff.itemModifiedAttributes.getOriginal(x.name)
            slider = AttributeSlider(self, value, min, max)
            mainSizer.Add(wx.StaticText(self, wx.ID_ANY, x.displayName), 1, wx.ALL | wx.EXPAND, 0)
            mainSizer.Add(slider, 1, wx.ALL | wx.EXPAND, 0)
            mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0, wx.ALL | wx.EXPAND, 0)


        self.SetSizer(mainSizer)
        self.Layout()
