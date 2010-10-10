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

import wx
import copy

class PyGauge(wx.PyWindow):
    """
    This class provides a visual alternative for `wx.Gauge`. It currently
    only support determinant mode (see SetValue and SetRange)
    """

    def __init__(self, parent, id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(-1,30), style=0):
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
        self._barColour    = self._barColourSorted   = [wx.Colour(212,228,255)]
        self._barGradient  = self._barGradientSorted = None

        self._border_padding = 0
        self._range = range
        self._value = 0

        self._fractionDigits = 0

        self._timerId = wx.NewId()
        self._timer = None

        self._oldValue = 0

        self._animDuration = 600
        self._animStep = 0
        self._period = 25
        self._animValue = 0


        self._percentage = 0
        self._oldPercentage = 0


        self.SetBarGradient((wx.Colour(119,119,119),wx.Colour(153,153,153)))
        self.SetBackgroundColour(wx.Colour(51,51,51))
        self._tooltip = wx.ToolTip("")
        self.SetToolTip(self._tooltip)
        self._tooltip.SetTip("0/0")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_TIMER, self.OnTimer)


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
        if type(colour) != type([]):
            self._barColour = [colour]
        else:
            self._barColour = list(colour)

    SetBarColor = SetBarColour
    GetBarColor = GetBarColour

    def SetFractionDigits(self, digits):
        self._fractionDigits=digits

    def GetBarGradient(self):
        """ Returns a tuple containing the gradient start and end colours. """

        if self._barGradient == None:
            return None

        return self._barGradient[0]

    def SetBarGradient(self, gradient = None):
        """
        Sets the bar gradient. This overrides the BarColour.

        :param `gradient`: a tuple containing the gradient start and end colours.
        """
        if gradient == None:
            self._barGradient = None
        else:
            if type(gradient) != type([]):
                self._barGradient = [gradient]
            else:
                self._barGradient = list(gradient)


    def GetBorderPadding(self):
        """ Gets the border padding. """

        return self._border_padding

    def SetBorderPadding(self, padding):
        """
        Sets the border padding.

        :param `padding`: pixels between the border and the progress bar.
        """

        self._border_padding = padding


    def GetRange(self):
        """ Returns the maximum value of the gauge. """

        return self._range

    def Animate(self):
        if not self._timer:
            self._timer = wx.Timer(self, self._timerId)
        self._animStep = 0
        self._timer.Start(self._period)

    def SetRange(self, range, reinit = False):
        """
        Sets the range of the gauge. The gauge length is its
        value as a proportion of the range.

        :param `range`: The maximum value of the gauge.
        """

        if self._range == range:
            return

        range = float(range)

        if range <= 0:
            self._range = 0.01
        else:
            self._range = range

        if reinit is False:
            self._oldPercentage = self._percentage
            self._percentage = (self._value/self._range) * 100
        else:
            self._oldPercentage = self._percentage
            self._percentage = 0
            self._value = 0

        self.Animate()


        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range if self._range >0.01 else 0))


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
        self._percentage = (self._value/self._range) * 100

        self.Animate()

        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range))

    def SetValueRange(self, value, range, reinit = False):

        range = float(range)

        if range <= 0:
            self._range = 0.01
        else:
            self._range = range

        value = float(value)

        self._value = value
        if value < 0:
            self._value = float(0)

        if reinit is False:
            self._oldPercentage = self._percentage
            self._percentage = (self._value/self._range) * 100

        else:
            self._oldPercentage = self._percentage
            self._percentage = 0


        self.Animate()
        self._tooltip.SetTip("%.2f/%.2f" % (self._value, self._range if self._range >0.01 else 0))

    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for L{PyGauge}.

        :param `event`: a `wx.EraseEvent` event to be processed.

        :note: This method is intentionally empty to reduce flicker.
        """

        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for L{PyGauge}.

        :param `event`: a `wx.PaintEvent` event to be processed.
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
            rect.Deflate(pad,pad)

        if self.GetBarGradient():

            c1,c2 = self.GetBarGradient()
            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)
            r = copy.copy(rect)
            r.width = w
            r.height = r.height/2+1

            pv = value

            if pv <= 100:
                c1 = map(lambda t: sum(t), zip(c1, (0,pv/3,-pv,0)))
                c2 = map(lambda t: sum(t), zip(c2, (0,pv/3,-pv,0)))
            else:
                if pv <= 105:
                    xv = pv -100
                    c1 = map(lambda t: sum(t), zip(c1, (0,100/3,-100,0)))
                    c1 = map(lambda t: sum(t), zip(c1, (xv*10,-xv*20,0,0)))

                    c2 = map(lambda t: sum(t), zip(c2, (0,100/3,-100,0)))
                    c2 = map(lambda t: sum(t), zip(c2, (xv*10,-xv*20,0,0)))

                else:
                    pv = 106
                    xv = pv -100

                    c2 = map(lambda t: sum(t), zip(c2, (0,100/3,-100,0)))
                    c2 = map(lambda t: sum(t), zip(c2, (xv*15,-xv*20,0,0)))

                    c1 = wx.Colour(255,0,0)

            dc.GradientFillLinear(r, c1, c2, wx.SOUTH)
            r.top = r.height
            dc.GradientFillLinear(r, c1, c2, wx.NORTH)
        else:
            colour=self.GetBarColour()
            dc.SetBrush(wx.Brush(colour))
            dc.SetPen(wx.Pen(colour))
            if value > 100:
                w = rect.width
            else:
                w = rect.width * (float(value) / 100)
            r = copy.copy(rect)
            r.width = w
            dc.DrawRectangleRect(r)

        dc.SetTextForeground(wx.Colour(255,255,255))

        standardFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if "__WXMAC__" in  wx.PlatformInfo :
            fsize = 9
        else:
            fsize = 8
        standardFont.SetPointSize(fsize)
        dc.SetFont(standardFont)


        formatStr = "{0:." + str(self._fractionDigits) + "f}%"
        dc.DrawLabel(formatStr.format(value), rect, wx.ALIGN_CENTER)

    def OUT_QUAD (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)

        t/=d

        return -c *(t)*(t-2) + b

    def OUT_BOUNCE (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)

        t/=d

        if ((t) < (1/2.75)):
            return c*(7.5625*t*t) + b
        else:
            if (t < (2/2.75)):
                t-=(1.5/2.75)
                return c*(7.5625*t*t + .75) + b
            else:
                if (t < (2.5/2.75)):
                    t-=(2.25/2.75)
                    return c*(7.5625*(t)*t + .9375) + b
                else:
                    t-=(2.625/2.75)
                    return c*(7.5625*(t)*t + .984375) + b



    def OnTimer(self,event):
        """
        Handles the ``wx.EVT_TIMER`` event for L{PyfaGauge}.

        :param `event`: a timer event
        """
        oldValue=self._oldPercentage
        value=self._percentage

        if oldValue < value:
            direction = 1
            start = 0
            end = value-oldValue
        else:
            direction = -1
            start = 0
            end = oldValue - value

        step=self.OUT_QUAD(self._animStep, start, end, self._animDuration)
        self._animStep += self._period

        if self._timerId == event.GetId():
            stop_timer = False

            if self._animStep > self._animDuration:
                stop_timer = True

            if direction == 1:
                if (oldValue+step) < value:
                    self._animValue = oldValue+step
                else:
                    stop_timer = True
            else:
                if (oldValue-step) > value:
                    self._animValue = oldValue-step
                else:
                    stop_timer = True

            if stop_timer:
                self._timer.Stop()

            self.Refresh()

