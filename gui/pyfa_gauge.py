# ===============================================================================
# PyfaGauge is a generic Gauge implementation tailored for pyfa (the Python
# Fitting Assistant). It uses the easeOutQuad equation from
# caurina.transitions.Tweener to do animations
#
# ToDo: make SetGradient(<value, colour start, colour end)
# ToDo: make a solid gradient (not to->from and not dependant on value)
# ToDo: fix 0 range (currently resets range to 0.01, but this causes problems if
#       we really set range at 0.01). Perhaps make it -1 and test percentage as
#       a negativeor something.
# ToDo: possibly devise a way to determine transition percents on init
#       (currently hardcoded)
#
# ===============================================================================

import copy
import wx

from gui.utils import color as color_utils
from gui.utils import draw, anim_effects
from service.fit import Fit


class PyGauge(wx.Window):
    def __init__(self, parent, font, max_range=100, size=(-1, 30), *args,
                 **kargs):

        super().__init__(parent, size=size, *args, **kargs)

        self._size = size

        self._border_colour = wx.BLACK
        self._bar_colour = None
        self._bar_gradient = None

        self._border_padding = 0
        self._max_range = max_range
        self._value = 0

        self._fraction_digits = 0

        self._timer_id = wx.NewId()
        self._timer = None

        self._oldValue = 0

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

        self.gradient_effect = -35

        self._percentage = 0
        self._old_percentage = 0
        self._show_remaining = False

        self.font = font

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
        # sFit = Fit.getInstance()
        if True:
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
        if self._value == value:
            return

        self._old_percentage = self._percentage
        self._value = value

        if value < 0:
            self._value = 0

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
        if value < 0:
            self._value = float(0)

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

        if self.GetBarColour():
            # if we have a bar color set, then we will use this

            colour = self.GetBarColour()
            dc.SetBrush(wx.Brush(colour))
            dc.SetPen(wx.Pen(colour))

            # calculate width of bar and draw it
            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)

            r = copy.copy(rect)
            r.width = w
            dc.DrawRectangle(r)
        else:
            # if bar color is not set, then we use pre-defined transitions
            # for the colors based on the percentage value

            # calculate width of bar
            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)
            r = copy.copy(rect)
            r.width = w

            # determine transition range number and calculate xv (which is the
            # progress between the two transition ranges)
            pv = value
            if pv <= 100:
                xv = pv / 100
                transition = 0
            elif pv <= 101:
                xv = pv - 100
                transition = 1
            elif pv <= 103:
                xv = (pv - 101) / 2
                transition = 2
            elif pv <= 105:
                xv = (pv - 103) / 2
                transition = 3
            else:
                pv = 106
                xv = pv - 100
                transition = -1

            if transition != -1:
                start_color, end_color = self.transition_colors[transition]
                color = color_utils.CalculateTransition(start_color, end_color,
                                                        xv)
            else:
                color = wx.Colour(191, 48, 48)  # dark red

            color_factor = self.gradient_effect / 100
            mid_factor = (self.gradient_effect / 2) / 100

            if self.gradient_effect > 0:
                gradient_color = color_utils.Brighten(color, color_factor)
                gradient_mid = color_utils.Brighten(color, mid_factor)
            else:
                gradient_color = color_utils.Darken(color, color_factor * -1)
                gradient_mid = color_utils.Darken(color, mid_factor * -1)

            # draw bar
            gradient_bitmap = draw.DrawGradientBar(
                r.width,
                r.height,
                gradient_mid,
                color,
                gradient_color
            )
            dc.DrawBitmap(gradient_bitmap, r.left, r.top)

        # font stuff begins here
        dc.SetFont(self.font)

        # determine shadow position
        r = copy.copy(rect)
        r.left += 1
        r.top += 1

        if self._max_range == 0.01 and self._value > 0:
            format = u'\u221e'  # infinity symbol
            # drop shadow
            dc.SetTextForeground(wx.Colour(80, 80, 80))  # dark grey
            dc.DrawLabel(format, r, wx.ALIGN_CENTER)
            # text
            dc.SetTextForeground(wx.WHITE)
            dc.DrawLabel(format, rect, wx.ALIGN_CENTER)
        else:
            if not self.GetBarColour() and self._show_remaining:
                # we only do these for gradients with mouse over
                range = self._max_range if self._max_range > 0.01 else 0
                value = range - self._value
                if value < 0:
                    label = "over"
                    value = -value
                else:
                    label = "left"
                format = "{0:." + str(self._fraction_digits) + "f} " + label
            else:
                format = "{0:." + str(self._fraction_digits) + "f}%"

            # drop shadow
            dc.SetTextForeground(wx.Colour(80, 80, 80))
            dc.DrawLabel(format.format(value), r, wx.ALIGN_CENTER)
            # text
            dc.SetTextForeground(wx.WHITE)
            dc.DrawLabel(format.format(value), rect, wx.ALIGN_CENTER)

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
    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump

    class MyPanel(wx.Panel):
        def __init__(self, parent, size=(500, 500)):
            wx.Panel.__init__(self, parent, size=size)
            box = wx.BoxSizer(wx.VERTICAL)

            # tests the colors of transition based on percentage used
            # list of test values (from 99 -> 106 in increments of 0.5)
            tests = [x for x in frange(99, 106.5, .5)]

            font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

            for i, value in enumerate(tests):
                self.gauge = PyGauge(self, font, size=(100, 25))
                self.gauge.SetValueRange(value, 100)
                self.gauge.SetFractionDigits(2)
                box.Add(self.gauge, 0, wx.ALL, 2)

            gauge = PyGauge(self, font, size=(100, 25))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(38, 133, 198))
            gauge.SetValue(59)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL, 2)

            gauge = PyGauge(self, font, size=(100, 5))
            gauge.SetBackgroundColour(wx.Colour(52, 86, 98))
            gauge.SetBarColour(wx.Colour(255, 128, 0))
            gauge.SetValue(59)
            gauge.SetFractionDigits(1)
            box.Add(gauge, 0, wx.ALL, 2)

            self.SetSizer(box)
            self.Layout()

            # see animation going backwards with last gauge
            wx.CallLater(2000, self.ChangeValues)

        def ChangeValues(self):
            self.gauge.SetValueRange(4, 100)

    class Frame(wx.Frame):
        def __init__(self, title, size=(500, 800)):
            wx.Frame.__init__(self, None, title=title, size=size)
            self.statusbar = self.CreateStatusBar()
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            panel = MyPanel(self, size=size)
            main_sizer.Add(panel)
            self.SetSizer(main_sizer)

    app = wx.App(redirect=False)   # Error messages go to popup window
    top = Frame("Test Chrome Tabs")
    top.Show()
    app.MainLoop()
