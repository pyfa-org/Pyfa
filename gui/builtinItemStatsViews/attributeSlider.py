import wx

class AttributeSlider(wx.Panel):
    # Slider which abstracts users values from internal values (because the built in slider does not deal with floats
    # and the like), based on http://wxpython-users.wxwidgets.narkive.com/ekgBzA7u/anyone-ever-thought-of-a-floating-point-slider

    def __init__(self, parent, baseValue, minMod, maxMod):
        wx.Panel.__init__(self, parent)

        self.parent = parent

        self.base_value = baseValue

        self.UserMinValue = minMod
        self.UserMaxValue = maxMod

        # The internal slider basically represents the percentage towards the end of the range. It has to be normalized
        # in this way, otherwise when we start off with a base, if the range is skewed to one side, the base value won't
        # be centered. We use a range of -100,100 so that we can depend on the SliderValue to contain the percentage
        # toward one end

        self.SliderMinValue = -100
        self.SliderMaxValue = 100
        self.SliderValue = 0

        self.statxt1 = wx.StaticText(self, wx.ID_ANY, 'left',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_LEFT)
        self.statxt2 = wx.StaticText(self, wx.ID_ANY, 'middle',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.statxt3 = wx.StaticText(self, wx.ID_ANY, 'right',
        style=wx.ST_NO_AUTORESIZE | wx.ALIGN_RIGHT)

        self.statxt1.SetLabel("{0:.3f}".format(self.UserMinValue * self.base_value))
        self.statxt1.SetToolTip("{0:+f}%".format((1-self.UserMinValue)*-100))
        self.statxt2.SetLabel("{0:.3f}".format(self.base_value))
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

        # The slkider value tells us when mod we're going to use, depending on its sign
        if self.SliderValue < 0:
            mod = self.UserMinValue
        elif self.SliderValue > 0:
            mod = self.UserMaxValue
        else:
            mod = 1

        # Get the slider value percentage as an absolute value
        slider_mod = abs(self.SliderValue) / 100

        # Gets our new mod by use the slider's percentage to determine where in the spectrum it is
        new_mod = mod + ((1-mod)-((1-mod) * slider_mod))

        # Modifies our base vale, to get out modified value
        newValue = new_mod * self.base_value

        if mod == 1:
            self.statxt2.SetLabel("{0:.3f}".format(newValue))
        else:
            self.statxt2.SetLabel("{0:.3f} ({1:+.3f})".format(newValue, newValue-self.base_value,))
            self.statxt2.SetToolTip("{0:+f}%".format(newValue))

    def SetValue(self, value):
        # todo: check this against values that might be 2.5x and whatnot
        mod = value / self.base_value
        if mod < 1:
            modEnd = -1 * self.UserMinValue
            sliderMod = (modEnd / mod) * 100
        elif mod > 1:
            modEnd = self.UserMaxValue
            sliderMod = ((mod-1)/(modEnd-1)) * 100

        self.slider.SetValue(sliderMod)

    def CalculateUserValue(self):
        # this will just take the slider value and calculate what the user needs to see as their value.
        pass


class TestAttributeSlider(wx.Frame):

    def __init__(self, parent, id):
        title = 'Slider...'
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        sty = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, title, pos, size, sty)

        self.panel = AttributeSlider(self, 200, .80, 1.5)
        self.panel.SetValue(160)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = TestAttributeSlider(None, wx.ID_ANY)
    frame.Show()
    app.MainLoop()
