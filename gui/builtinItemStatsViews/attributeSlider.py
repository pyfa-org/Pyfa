import math

import wx
import wx.lib.newevent

from gui.attribute_gauge import AttributeGauge
from eos.utils.float import floatUnerr

_ValueChanged, EVT_VALUE_CHANGED = wx.lib.newevent.NewEvent()


class AttributeSliderChangeEvent:
    def __init__(self, obj, old_value, new_value, old_percentage, new_percentage, affect_modified_flag=True):
        self.__obj = obj
        self.__old = old_value
        self.__new = new_value
        self.__old_percent = old_percentage
        self.__new_percent = new_percentage
        self.__affect_modified_flag = affect_modified_flag

    def GetObj(self):
        return self.__obj

    def GetOldValue(self):
        return self.__old

    def GetValue(self):
        return self.__new

    def GetOldPercentage(self):
        return self.__old_percent

    def GetPercentage(self):
        return self.__new_percent

    @property
    def AffectsModifiedFlag(self):
        return self.__affect_modified_flag

    Object = property(GetObj)
    OldValue = property(GetOldValue)
    Value = property(GetValue)
    OldPercentage = property(GetOldPercentage)
    Percentage = property(GetPercentage)


class ValueChanged(_ValueChanged, AttributeSliderChangeEvent):
    def __init__(self, obj, old_value, new_value, old_percentage, new_percentage, affect_modified_flag=True):
        _ValueChanged.__init__(self)
        AttributeSliderChangeEvent.__init__(self, obj, old_value, new_value, old_percentage, new_percentage, affect_modified_flag=affect_modified_flag)


class AttributeSlider(wx.Panel):
    # Slider which abstracts users values from internal values (because the built in slider does not deal with floats
    # and the like), based on http://wxpython-users.wxwidgets.narkive.com/ekgBzA7u/anyone-ever-thought-of-a-floating-point-slider

    def __init__(self, parent, baseValue, minValue, maxValue, inverse=False, id=-1):
        wx.Panel.__init__(self, parent, id=id)

        self.parent = parent

        self.base_value = baseValue

        self.UserMinValue = minValue
        self.UserMaxValue = maxValue

        self.inverse = inverse

        def getStep(valRange):
            """
            Find step for the passed range, which is based on 1, 2 or 5.
            Step returned will make sure that range fits 10..50 of them,
            as close to 10 as possible.
            """
            steps = {1: None, 2: None, 5: None}
            for baseInc in steps:
                baseIncAmount = valRange / baseInc
                incScale = math.floor(math.log10(baseIncAmount) - 1)
                steps[baseInc] = baseInc * 10 ** incScale
            chosenBase = min(steps, key=lambda base: valRange / steps[base])
            chosenStep = steps[chosenBase]
            if inverse:
                chosenStep *= -1
            return chosenStep

        def getDigitPlaces(minValue, maxValue):
            minDigits = 3
            maxDigits = 5
            currentDecision = minDigits
            for value in (floatUnerr(minValue), floatUnerr(maxValue)):
                for currentDigit in range(minDigits, maxDigits + 1):
                    if round(value, currentDigit) == value:
                        if currentDigit > currentDecision:
                            currentDecision = currentDigit
                        break
                # Max decimal places we can afford to show was not enough
                else:
                     return maxDigits
            return currentDecision

        self.ctrl = wx.SpinCtrlDouble(self, min=minValue, max=maxValue, inc=getStep(maxValue - minValue))
        self.ctrl.SetDigits(getDigitPlaces(minValue, maxValue))

        self.ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.UpdateValue)
        # GTK scrolls spinboxes with mousewheel, others do not
        if "wxGTK" not in wx.PlatformInfo:
            self.ctrl.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        self.slider = AttributeGauge(self, size=(-1, 8))

        b = 4
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(self.ctrl, 0, wx.LEFT | wx.RIGHT | wx.CENTER, b)
        vsizer1.Add(self.slider, 0, wx.EXPAND | wx.ALL , b)

        self.SetSizerAndFit(vsizer1)
        self.parent.SetClientSize((500, vsizer1.GetSize()[1]))

    def GetValue(self):
        return self.ctrl.GetValue()

    def UpdateValue(self, evt):
        self.SetValue(self.GetValue())
        evt.Skip()

    def SetValue(self, value, post_event=True, affect_modified_flag=True):
        self.ctrl.SetValue(value)
        invert_factor = -1 if self.inverse else 1
        try:
            if value >= self.base_value:
                slider_percentage = (value - self.base_value) / (self.UserMaxValue - self.base_value) * 100 * invert_factor
            else:
                slider_percentage = (value - self.base_value) / (self.base_value - self.UserMinValue) * 100 * invert_factor
        except ZeroDivisionError:
            slider_percentage = 0
        self.slider.SetValue(slider_percentage)
        if post_event:
            wx.PostEvent(self, ValueChanged(self, None, value, None, slider_percentage, affect_modified_flag=affect_modified_flag))

    def OnMouseWheel(self, evt):
        if evt.GetWheelRotation() > 0 and evt.GetWheelAxis() == wx.MOUSE_WHEEL_VERTICAL:
            self.SetValue(self.ctrl.Value + self.ctrl.Increment)
        elif evt.GetWheelRotation() < 0 and evt.GetWheelAxis() == wx.MOUSE_WHEEL_VERTICAL:
            self.SetValue(self.ctrl.Value - self.ctrl.Increment)
        else:
            evt.Skip()

    def OnWindowClose(self):
        # Stop animations to prevent crashes when window is
        # closed while animation is in progress
        self.slider.FreezeAnimation()
