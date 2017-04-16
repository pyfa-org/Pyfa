# --------------------------------------------------------------------------------- #
# PYFAGAUGE wxPython IMPLEMENTATION
#
# Darriele, @ 08/30/2010
# Updated: 09/07/2010
# Based on AWG : pygauge code
# --------------------------------------------------------------------------------- #

"""
PyfaGauge is a generic Gauge implementation tailored for PYFA (Python Fitting Assistant)
It uses the easeOutQuad equation from caurina.transitions.Tweener to do the animation stuff
"""

# noinspection PyPackageRequirements
import wx
import copy

from gui.utils import colorUtils
import gui.utils.drawUtils as drawUtils
import gui.utils.animEffects as animEffects
import gui.utils.fonts as fonts

from service.fit import Fit


class PyGauge(wx.PyWindow):
    """
    This class provides a visual alternative for `wx.Gauge`. It currently
    only support determinant mode (see SetValue and SetRange)
    """

    def __init__(self, parent, id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(-1, 30), style=0):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform.
        """

        wx.PyWindow.__init__(self, parent, id, pos, size, style)

        self._size = size

        self._border_colour = wx.BLACK
        self._barColour = self._barColourSorted = [wx.Colour(212, 228, 255)]
        self._barGradient = self._barGradientSorted = None

        self._border_padding = 0
        self._range = range
        self._value = 0

        self._fractionDigits = 0

        self._timerId = wx.NewId()
        self._timer = None

        self._oldValue = 0

        self._animDuration = 500
        self._animStep = 0
        self._period = 20
        self._animValue = 0
        self._animDirection = 0
        self.animEffect = animEffects.OUT_QUAD

        self.transitionsColors = [(wx.Colour(191, 191, 191, 255), wx.Colour(96, 191, 0, 255)),
                                  (wx.Colour(191, 167, 96, 255), wx.Colour(255, 191, 0, 255)),
                                  (wx.Colour(255, 191, 0, 255), wx.Colour(255, 128, 0, 255)),
                                  (wx.Colour(255, 128, 0, 255), wx.Colour(255, 0, 0, 255))]
        self.gradientEffect = -35

        self._percentage = 0
        self._oldPercentage = 0
        self._showRemaining = False

        self.font = wx.Font(fonts.NORMAL, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

        self.SetBarGradient((wx.Colour(119, 119, 119), wx.Colour(153, 153, 153)))
        self.SetBackgroundColour(wx.Colour(51, 51, 51))
        self._tooltip = wx.ToolTip("")
        self.SetToolTip(self._tooltip)
        self._tooltip.SetTip("0.00/100.00")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnWindowEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnWindowLeave)

    def OnWindowEnter(self, event):
        self._showRemaining = True
        self.Refresh()

    def OnWindowLeave(self, event):
        self._showRemaining = False
        self.Refresh()

    def DoGetBestSize(self):
        """
        Overridden base class virtual. Determines the best size of the
        button based on the label and bezel size.
        """

        return wx.Size(self._size[0], self._size[1])

    def GetBorderColour(self):
        return self._border_colour

    def SetBorderColour(self, colour):
        self._border_colour = colour

    SetBorderColor = SetBorderColour
    GetBorderColor = GetBorderColour

    def GetBarColour(self):
        return self._barColour[0]

    def SetBarColour(self, colour):
        if not isinstance(colour, list):
            self._barColour = [colour]
        else:
            self._barColour = list(colour)

    SetBarColor = SetBarColour
    GetBarColor = GetBarColour

    def SetFractionDigits(self, digits):
        self._fractionDigits = digits

    def GetBarGradient(self):
        """ Returns a tuple containing the gradient start and end colours. """

        if self._barGradient is None:
            return None

        return self._barGradient[0]

    def SetBarGradient(self, gradient=None):
        """
        Sets the bar gradient. This overrides the BarColour.

        :param gradient: a tuple containing the gradient start and end colours.
        """
        if gradient is None:
            self._barGradient = None
        else:
            if not isinstance(gradient, list):
                self._barGradient = [gradient]
            else:
                self._barGradient = list(gradient)

    def GetBorderPadding(self):
        """ Gets the border padding. """

        return self._border_padding

    def SetBorderPadding(self, padding):
        """
        Sets the border padding.

        :param padding: pixels between the border and the progress bar.
        """

        self._border_padding = padding

    def GetRange(self):
        """ Returns the maximum value of the gauge. """

        return self._range

    def Animate(self):
        sFit = Fit.getInstance()
        if sFit.serviceFittingOptions["enableGaugeAnimation"]:
            if not self._timer:
                self._timer = wx.Timer(self, self._timerId)
            self._animStep = 0
            self._timer.Start(self._period)
        else:
            self._animValue = self._percentage
            self.Refresh()

    def SetRange(self, range, reinit=False):
        """
        Sets the range of the gauge. The gauge length is its
        value as a proportion of the range.

        :param reinit:
        :param range: The maximum value of the gauge.
        """

        if self._range == range:
            return

        range_ = float(range)

        if range_ <= 0:
            self._range = 0.01
        else:
            self._range = range_

        if reinit is False:
            self._oldPercentage = self._percentage
            self._percentage = (self._value / self._range) * 100
        else:
            self._oldPercentage = self._percentage
            self._percentage = 0
            self._value = 0

        self.Animate()

        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range if self._range > 0.01 else 0))

    def GetValue(self):
        """ Returns the current position of the gauge. """

        return self._value

    def SetValue(self, value):
        """ Sets the current position of the gauge. """
        if self._value == value:
            return

        value = float(value)
        self._oldPercentage = self._percentage
        self._value = value
        if value < 0:
            self._value = 0
        self._percentage = (self._value / self._range) * 100

        self.Animate()

        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range))

    def SetValueRange(self, value, range, reinit=False):
        if self._value == value and self._range == range:
            return

        range_ = float(range)

        if range_ <= 0:
            self._range = 0.01
        else:
            self._range = range_

        value = float(value)

        self._value = value
        if value < 0:
            self._value = float(0)

        if reinit is False:
            self._oldPercentage = self._percentage
            self._percentage = (self._value / self._range) * 100

        else:
            self._oldPercentage = self._percentage
            self._percentage = 0

        self.Animate()
        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range if self._range > 0.01 else 0))

    @staticmethod
    def OnEraseBackground(event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for L{PyGauge}.

        :param event: a `wx.EraseEvent` event to be processed.

        :note: This method is intentionally empty to reduce flicker.
        """

        pass

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for L{PyGauge}.

        :param event: a `wx.PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        rect = self.GetClientRect()

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        colour = self.GetBackgroundColour()

        dc.SetBrush(wx.Brush(colour))
        dc.SetPen(wx.Pen(colour))

        dc.DrawRectangleRect(rect)

        value = self._percentage
        if self._timer:
            if self._timer.IsRunning():
                value = self._animValue

        if self._border_colour:
            dc.SetPen(wx.Pen(self.GetBorderColour()))
            dc.DrawRectangleRect(rect)
            pad = 1 + self.GetBorderPadding()
            rect.Deflate(pad, pad)

        if self.GetBarGradient():

            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)
            r = copy.copy(rect)
            r.width = w

            if r.width > 0:
                # If we draw it with zero width, GTK throws errors. This way,
                # only draw it if the gauge will actually show something.
                # We stick other calculations in this block to avoid wasting
                # time on them if not needed. See GH issue #282

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
                    colorS, colorE = self.transitionsColors[transition]
                    color = colorUtils.CalculateTransitionColor(colorS, colorE, xv)
                else:
                    color = wx.Colour(191, 48, 48)

                if self.gradientEffect > 0:
                    gcolor = colorUtils.BrightenColor(color, float(self.gradientEffect) / 100)
                    gMid = colorUtils.BrightenColor(color, float(self.gradientEffect / 2) / 100)
                else:
                    gcolor = colorUtils.DarkenColor(color, float(-self.gradientEffect) / 100)
                    gMid = colorUtils.DarkenColor(color, float(-self.gradientEffect / 2) / 100)

                gBmp = drawUtils.DrawGradientBar(r.width, r.height, gMid, color, gcolor)
                dc.DrawBitmap(gBmp, r.left, r.top)

        else:
            colour = self.GetBarColour()
            dc.SetBrush(wx.Brush(colour))
            dc.SetPen(wx.Pen(colour))
            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)
            r = copy.copy(rect)
            r.width = w
            dc.DrawRectangleRect(r)

        dc.SetFont(self.font)

        r = copy.copy(rect)
        r.left += 1
        r.top += 1
        if self._range == 0.01 and self._value > 0:
            formatStr = u'\u221e'
            dc.SetTextForeground(wx.Colour(80, 80, 80))
            dc.DrawLabel(formatStr, r, wx.ALIGN_CENTER)

            dc.SetTextForeground(wx.Colour(255, 255, 255))
            dc.DrawLabel(formatStr, rect, wx.ALIGN_CENTER)
        else:
            if self.GetBarGradient() and self._showRemaining:
                range = self._range if self._range > 0.01 else 0
                value = range - self._value
                if value < 0:
                    label = "over"
                    value = -value
                else:
                    label = "left"
                formatStr = "{0:." + str(self._fractionDigits) + "f} " + label

            else:
                formatStr = "{0:." + str(self._fractionDigits) + "f}%"

            dc.SetTextForeground(wx.Colour(80, 80, 80))
            dc.DrawLabel(formatStr.format(value), r, wx.ALIGN_CENTER)

            dc.SetTextForeground(wx.Colour(255, 255, 255))
            dc.DrawLabel(formatStr.format(value), rect, wx.ALIGN_CENTER)

    def OnTimer(self, event):
        """
        Handles the ``wx.EVT_TIMER`` event for L{PyfaGauge}.

        :param event: a timer event
        """
        oldValue = self._oldPercentage
        value = self._percentage
        start = 0

        direction = 1 if oldValue < value else -1

        end = direction * (value - oldValue)

        self._animDirection = direction
        step = self.animEffect(self._animStep, start, end, self._animDuration)

        self._animStep += self._period

        if self._timerId == event.GetId():
            stop_timer = False

            if self._animStep > self._animDuration:
                stop_timer = True

            if direction == 1:
                if (oldValue + step) < value:
                    self._animValue = oldValue + step
                else:
                    stop_timer = True
            else:
                if (oldValue - step) > value:
                    self._animValue = oldValue - step

                else:
                    stop_timer = True

            if stop_timer:
                self._timer.Stop()

            self.Refresh()
