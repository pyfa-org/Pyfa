import copy
import wx
import math

from gui.utils import color as color_utils
from gui.utils import draw, anim_effects
from service.fit import Fit

# todo: clean class up. Took from pyfa gauge, has a bunch of extra shit we don't need


class AttributeGauge(wx.Window):
    def __init__(self, parent, max_range=100, animate=True, leading_edge=True, edge_on_neutral=True, guide_lines=False, size=(-1, 30), *args,
                 **kargs):

        super().__init__(parent, size=size, *args, **kargs)

        self._size = size

        self.guide_lines = guide_lines

        self._border_colour = wx.BLACK
        self._bar_colour = None
        self._bar_gradient = None

        self.leading_edge = leading_edge
        self.edge_on_neutral = edge_on_neutral

        self._border_padding = 0
        self._max_range = max_range
        self._value = 0

        self._fraction_digits = 0

        self._timer_id = wx.NewId()
        self._timer = None

        self._oldValue = 0

        self._animate = animate
        self._anim_duration = 500
        self._anim_step = 0
        self._period = 20
        self._anim_value = 0
        self._anim_direction = 0
        self.anim_effect = anim_effects.OUT_QUAD

        # transition colors used based on how full (or overfilled) the gauge is.
        self.transition_colors = [
            (wx.Colour(191, 191, 191), wx.Colour(96, 191, 0)),  # < 0-100%
            (wx.Colour(191, 167, 96), wx.Colour(255, 191, 0)),  # < 100-101%
            (wx.Colour(255, 191, 0), wx.Colour(255, 128, 0)),  # < 101-103%
            (wx.Colour(255, 128, 0), wx.Colour(255, 0, 0))  # < 103-105%
        ]

        self.goodColor = wx.Colour(96, 191, 0)
        self.badColor = wx.Colour(255, 64, 0)

        self.gradient_effect = -35

        self._percentage = 0
        self._old_percentage = 0
        self._show_remaining = False

        self.SetBackgroundColour(wx.Colour(51, 51, 51))

        self._tooltip = wx.ToolTip("0.00/100.00")
        self.SetToolTip(self._tooltip)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def OnEraseBackground(self, event):
        pass

    def OnWindowEnter(self, event):
        self._show_remaining = True
        self.Refresh()

    def OnWindowLeave(self, event):
        self._show_remaining = False
        self.Refresh()

    def GetBorderColour(self):
        return self._border_colour

    def SetBorderColour(self, colour):
        self._border_colour = colour

    def GetBarColour(self):
        return self._bar_colour

    def SetBarColour(self, colour):
        self._bar_colour = colour

    def SetFractionDigits(self, digits):
        self._fraction_digits = digits

    def GetBarGradient(self):
        if self._bar_gradient is None:
            return None

        return self._bar_gradient[0]

    def SetBarGradient(self, gradient=None):
        if gradient is None:
            self._bar_gradient = None
        else:
            if not isinstance(gradient, list):
                self._bar_gradient = [gradient]
            else:
                self._bar_gradient = list(gradient)

    def GetBorderPadding(self):
        return self._border_padding

    def SetBorderPadding(self, padding):
        self._border_padding = padding

    def GetRange(self):
        """ Returns the maximum value of the gauge. """
        return self._max_range

    def Animate(self):
        if self._animate:
            if not self._timer:
                self._timer = wx.Timer(self, self._timer_id)

            self._anim_step = 0
            self._timer.Start(self._period)
        else:
            self._anim_value = self._percentage
            self.Refresh()

    def SetRange(self, range, reinit=False, animate=True):
        """
        Sets the range of the gauge. The gauge length is its
        value as a proportion of the range.
        """

        if self._max_range == range:
            return

        # we cannot have a range of zero (laws of physics, etc), so we set it
        if range <= 0:
            self._max_range = 0.01
        else:
            self._max_range = range

        if reinit is False:
            self._old_percentage = self._percentage
            self._percentage = (self._value / self._max_range) * 100
        else:
            self._old_percentage = self._percentage
            self._percentage = 0
            self._value = 0

        if animate:
            self.Animate()

        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._max_range if self._max_range > 0.01 else 0))

    def GetValue(self):
        return self._value

    def SetValue(self, value, animate=True):
        """ Sets the current position of the gauge. """

        print ("="*20, self._percentage)
        if self._value == value:
            return

        self._old_percentage = self._percentage
        self._value = value

        self._percentage = (self._value / self._max_range) * 100

        if animate:
            self.Animate()

        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._max_range))

    def SetValueRange(self, value, range, reinit=False):
        """ Set both value and range of the gauge. """
        range_ = float(range)

        if range_ <= 0:
            self._max_range = 0.01
        else:
            self._max_range = range_

        value = float(value)

        self._value = value

        if reinit is False:
            self._old_percentage = self._percentage
            self._percentage = (self._value / self._max_range) * 100

        else:
            self._old_percentage = self._percentage
            self._percentage = 0

        self.Animate()
        self._tooltip.SetTip("%.2f/%.2f" %
                             (self._value, self._max_range if float(self._max_range) > 0.01 else 0))

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        rect = self.GetClientRect()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        colour = self.GetBackgroundColour()

        dc.SetBrush(wx.Brush(colour))
        dc.SetPen(wx.Pen(colour))

        dc.DrawRectangle(rect)

        value = self._percentage

        if self._timer:
            if self._timer.IsRunning():
                value = self._anim_value

        if self._border_colour:
            dc.SetPen(wx.Pen(self.GetBorderColour()))
            dc.DrawRectangle(rect)
            pad = 1 + self.GetBorderPadding()
            rect.Deflate(pad, pad)

        if True:
            # if we have a bar color set, then we will use this
            colour = self.goodColor if value >= 0 else self.badColor

            is_even = rect.width % 2 == 0

            # the size of half our available drawing area (since we're only working in halves)
            half = (rect.width / 2)

            # calculate width of bar as a percentage of half the space
            w = abs(half * (value / 100))
            w = min(w, half)  # Ensure that we don't overshoot our drawing area
            w = math.ceil(w)  # round up to nearest pixel, this ensures that we don't lose representation for sub pixels

            # print("Percentage: {}\t\t\t\t\tValue: {}\t\t\t\t\tWidth: {}\t\t\t\t\tHalf: {}\t\t\t\t\tRect Width: {}".format(round(self._percentage, 3), round(value,3), w, half, rect.width))

            # set guide_lines every 10 pixels of the main gauge (not including borders)
            if self.guide_lines:
                for x in range(1, 20):
                    dc.SetBrush(wx.Brush(wx.LIGHT_GREY))
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY))
                    dc.DrawRectangle(x*10, 1, 1, rect.height)

            dc.SetBrush(wx.Brush(colour))
            dc.SetPen(wx.Pen(colour))

            # If we have an  even width, we can simply dedicate the middle-most pixels to both sides
            # However, if there is an odd width, the middle pixel is shared between the left and right gauge

            if value >= 0:
                padding = (half if is_even else math.ceil(half-1)) + 1
                dc.DrawRectangle(padding, 1, w, rect.height)
            else:
                padding = half - w + 1 if is_even else math.ceil(half)-(w-1)
                dc.DrawRectangle(padding, 1, w, rect.height)

            if self.leading_edge and (self.edge_on_neutral or value != 0):
                dc.SetPen(wx.Pen(wx.WHITE))
                dc.SetBrush(wx.Brush(wx.WHITE))

                if value > 0:
                    dc.DrawRectangle(min(padding + w, rect.width), 1, 1, rect.height)
                else:
                    dc.DrawRectangle(max(padding-1, 1), 1, 1, rect.height)

    def OnTimer(self, event):
        old_value = self._old_percentage
        value = self._percentage
        start = 0

        # -1 = left direction, 1 = right direction
        direction = 1 if old_value < value else -1

        end = direction * (value - old_value)

        self._anim_direction = direction
        step = self.anim_effect(self._anim_step, start, end, self._anim_duration)

        self._anim_step += self._period

        if self._timer_id == event.GetId():
            stop_timer = False

            if self._anim_step > self._anim_duration:
                stop_timer = True

            # add new value to the animation if we haven't reached our goal
            # otherwise, stop animation
            if direction == 1:
                if old_value + step < value:
                    self._anim_value = old_value + step
                else:
                    stop_timer = True
            else:
                if old_value - step > value:
                    self._anim_value = old_value - step
                else:
                    stop_timer = True

            if stop_timer:
                self._timer.Stop()

            self.Refresh()


if __name__ == "__main__":
    import random

    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump

    class MyPanel(wx.Panel):
        def __init__(self, parent, size=(500, 500)):
            wx.Panel.__init__(self, parent, size=size)
            box = wx.BoxSizer(wx.VERTICAL)

            font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

            self.gauge = gauge = AttributeGauge(self, size=(204, 4))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(100)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL|wx.CENTER, 10)

            self.gauge11 = gauge = AttributeGauge(self, size=(204, 6))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(100)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge12 = gauge = AttributeGauge(self, size=(204, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(100)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge13 = gauge = AttributeGauge(self, size=(204, 10))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(100)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.value = wx.StaticText(self, label="Text")
            box.Add(self.value, 0, wx.ALL | wx.CENTER, 5)

            self.btn = wx.Button(self, label="Toggle Timer")
            box.Add(self.btn, 0, wx.ALL | wx.CENTER, 5)
            self.btn.Bind(wx.EVT_BUTTON, self.ToggleTimer)

            self.spinCtrl = wx.SpinCtrl(self, min=-10000, max=10000)
            box.Add(self.spinCtrl, 0, wx.ALL | wx.CENTER, 5)
            self.spinCtrl.Bind(wx.EVT_SPINCTRL, self.UpdateValue)

            self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
            box.Add(self.m_staticline2, 0, wx.EXPAND, 5)

            self.spinCtrl2 = wx.SpinCtrl(self, min=0, max=10000)
            box.Add(self.spinCtrl2, 0, wx.ALL | wx.CENTER, 5)
            self.spinCtrl2.Bind(wx.EVT_SPINCTRL, self.UpdateValue2)

            box.Add(wx.StaticText(self, label="Large Even Pixel Test"), 0, wx.ALL | wx.CENTER, 5)

            guide_lines = False

            self.gauge2 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(204, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(2)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge3 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(204, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(-2)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            box.Add(wx.StaticText(self, label="Large Odd Pixel Test"), 0, wx.ALL | wx.CENTER, 5)

            self.gauge4 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(205, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(2)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge5 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(205, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(-2)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            box.Add(wx.StaticText(self, label="Small Even Pixel Test"), 0, wx.ALL | wx.CENTER, 5)

            self.gauge6 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(100, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(75)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge7 = gauge = AttributeGauge(self, guide_lines=guide_lines, size=(100, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(-75)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            box.Add(wx.StaticText(self, label="Small Odd Pixel Test"), 0, wx.ALL | wx.CENTER, 5)

            self.gauge8 = gauge = AttributeGauge(self, guide_lines=guide_lines, max_range=100, size=(101, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(1)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.gauge9 = gauge = AttributeGauge(self, guide_lines=guide_lines, max_range=100, size=(101, 8))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(-1)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL | wx.CENTER, 10)

            self.SetSizer(box)
            self.Layout()

            self.animTimer = wx.Timer(self, wx.NewId())
            self.Bind(wx.EVT_TIMER, self.OnTimer)

            self.animTimer.Start(1000)

        def ToggleTimer(self, evt):
            if self.animTimer.IsRunning:
                self.animTimer.Stop()
            else:
                self.animTimer.Start(1000)

        def UpdateValue(self, event):
            if self.animTimer.IsRunning:
                self.animTimer.Stop()
            num = self.spinCtrl.GetValue()
            self.gauge.SetValue(num)
            self.gauge11.SetValue(num)
            self.gauge12.SetValue(num)
            self.gauge13.SetValue(num)
            self.value.SetLabel(str(num))

        def UpdateValue2(self, event):
            num = self.spinCtrl2.GetValue()
            self.gauge2.SetValue(num)
            self.gauge3.SetValue(num*-1)
            self.gauge4.SetValue(num)
            self.gauge5.SetValue(num*-1)
            self.gauge6.SetValue(num)
            self.gauge7.SetValue(num*-1)
            self.gauge8.SetValue(num)
            self.gauge9.SetValue(num*-1)

        def OnTimer(self, evt):
            num = random.randint(-100,100)
            self.gauge.SetValue(num)
            self.gauge11.SetValue(num)
            self.gauge12.SetValue(num)
            self.gauge13.SetValue(num)
            self.value.SetLabel(str(num))

    class Frame(wx.Frame):
        def __init__(self, title, size=(500, 800)):
            wx.Frame.__init__(self, None, title=title, size=size)
            self.statusbar = self.CreateStatusBar()
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            panel = MyPanel(self, size=size)
            main_sizer.Add(panel)
            self.SetSizer(main_sizer)

    app = wx.App(redirect=False)   # Error messages go to popup window
    top = Frame("Test Attribute Bar")
    top.Show()
    app.MainLoop()
