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

class AttributeSlider(wx.Panel):
    # based on http://wxpython-users.wxwidgets.narkive.com/ekgBzA7u/anyone-ever-thought-of-a-floating-point-slider

    def __init__(self, parent, baseValue, minMod, maxMod):
        wx.Panel.__init__(self, parent)

        self.parent = parent

        self.mod = 100  # modifier for the underlying Slider (ensure we don't hit floats, which it doesn't support)
        self.base_value =  baseValue


        self.UserMinValue = minMod
        self.UserMaxValue = maxMod
        self.UserValue = 1

        self.SliderMinValue = self.UserMinValue * self.mod
        self.SliderMaxValue = self.UserMaxValue * self.mod
        self.SliderValue = self.UserValue * self.mod

        self.statxt1 = wx.StaticText(self, wx.ID_ANY, 'left',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_LEFT)
        self.statxt2 = wx.StaticText(self, wx.ID_ANY, 'middle',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.statxt3 = wx.StaticText(self, wx.ID_ANY, 'right',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_RIGHT)

        self.statxt1.SetLabel("{0:.3f}".format(self.UserMinValue * self.base_value))
        self.statxt1.SetToolTip("{0:+f}%".format((1-self.UserMinValue)*-100))
        self.statxt2.SetLabel("{0:.3f}".format(self.UserValue * self.base_value))
        self.statxt3.SetLabel("{0:.3f}".format(self.UserMaxValue * self.base_value))
        self.statxt3.SetToolTip("{0:+f}%".format((1-self.UserMaxValue)*-100))

        self.slider = wx.Slider(
            self, wx.ID_ANY,
            self.SliderValue,
            self.SliderMinValue,
            self.SliderMaxValue,
            style=wx.SL_HORIZONTAL)

        self.slider.SetTickFreq((self.SliderMaxValue - self.SliderMinValue) / 15)

        self.slider.Bind(wx.EVT_SCROLL, self.OnScroll)

        b = 20
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.statxt1, 1, wx.RIGHT, b)
        hsizer1.Add(self.statxt2, 1, wx.LEFT | wx.RIGHT, b)
        hsizer1.Add(self.statxt3, 1, wx.LEFT, b)

        b = 4
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(hsizer1, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(self.slider, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, b)

        self.SetSizerAndFit(vsizer1)
        self.parent.SetClientSize((500, vsizer1.GetSize()[1]))

    def OnScroll(self, event):
        self.SliderValue = self.slider.GetValue()
        self.UserValue = self.SliderValue / self.mod
        newValue = self.UserValue * self.base_value
        if self.UserValue == 1:
            self.statxt2.SetLabel("{0:.3f}".format(newValue))
        else:
            self.statxt2.SetLabel("{0:.3f} ({1:+.3f})".format(newValue, newValue-self.base_value,))
            self.statxt2.SetToolTip("{0:+f}%".format((1 - self.UserValue) * -100))


class TestAttributeSlider(wx.Frame):

    def __init__(self, parent, id):
        title = 'Slider...'
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        sty = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, title, pos, size, sty)

        self.panel = AttributeSlider(self, 200, 0.20, 1.3)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = TestAttributeSlider(None, wx.ID_ANY)
    frame.Show()
    app.MainLoop()
