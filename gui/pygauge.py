# --------------------------------------------------------------------------------- #
# PYGAUGE wxPython IMPLEMENTATION
#
# Mark Reed, @ 28 Jul 2010
# Latest Revision: 14 Apr 2010, 12.00 GMT
#
# TODO List
#
# 1. Indeterminate mode (see wx.Gauge)
# 2. Vertical bar
# 3. Bitmap support (bar, background)
# 4. UpdateFunction - Pass a function to PyGauge which will be called every X
#    milliseconds and the value will be updated to the returned value.
# 5. Currently the full gradient is drawn from 0 to value. Perhaps the gradient
#    should be drawn from 0 to range and clipped at 0 to value.
# 6. Add a label?
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To The:
#
# wxPython Mailing List!!!
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
PyGauge is a generic Gauge implementation.

Description
===========

PyGauge supports the determinate mode functions as wxGauge and adds an Update function
which takes a value and a time parameter. The value is added to the current value over
a period of time milliseconds.

Supported Platforms
===================

PyGauge has been tested on the following platforms:
  * Windows (Windows XP);

License And Version
===================

PyGauge is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 14 Apr 2010, 12.00 GMT

Version 0.1
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
        self._value = [0]
        self._valueSorted = [0]
        self._skipDigits = True
        self._timerId = wx.NewId()
        self._timer = None

        self._oldValue=0
        self._timerOn=0
        self._animDuration=250
        self._animStep=0
        self._period=25
        self._animValue=0
        self._overdrive=0
        self.SetBarGradient((wx.Colour(153,153,153),wx.Colour(204,204,204)))
        self.SetBackgroundColour(wx.Colour(102,102,102))


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

        self.SortForDisplay()

    SetBarColor = SetBarColour
    GetBarColor = GetBarColour

    def SetSkipDigitsFlag(self,flag):
        self._skipDigits=flag

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

            self.SortForDisplay()


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

    def SetRange(self, range):
        """
        Sets the range of the gauge. The gauge length is its
        value as a proportion of the range.

        :param `range`: The maximum value of the gauge.
        """

        if range <= 0:
            raise Exception("ERROR:\n Gauge range must be greater than 0.")

        self._range = range


    def GetValue(self):
        """ Returns the current position of the gauge. """

        return self._value[0]

    def SetValue(self, value):
        """ Sets the current position of the gauge. """
        if self._value[0] == value:
            self.SortForDisplay()
            self.Refresh()
        else:    
            self._oldValue = self._value[0]
            if type(value) != type([]):
                self._value = [value]
            else:
                self._value = list(value)

            if value > self._range:
                self._overdrive = value
                self._value[0] = self._range
            else:
                self._overdrive = value
        
            if not self._timer:
                self._timer = wx.Timer(self, self._timerId)
            self._animStep = 0
            self._timer.Start(self._animStep)

        for v in self._value:
            if v < 0 or v > self._range:
                raise Exception("ERROR:\n Gauge value must be between 0 and it's range. ")


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

        if self._timerOn == 1:
            value = self._animValue
        else:
            value = self._value[0]
        if self._border_colour:
            dc.SetPen(wx.Pen(self.GetBorderColour()))
            dc.DrawRectangleRect(rect)
            pad = 1 + self.GetBorderPadding()
            rect.Deflate(pad,pad)


        if self.GetBarGradient():
            for i, gradient in enumerate(self._barGradientSorted):
                if self._overdrive > self._range:
                    c1 =wx.Colour(255,33,33)
                    c2 =wx.Colour(255,33,33)
                else:
                    c1,c2 = gradient

                w = rect.width * (float(value) / self._range)
                r = copy.copy(rect)
                r.width = w
                dc.GradientFillLinear(r, c1, c2, wx.EAST)
        else:
            for i, colour in enumerate(self._barColourSorted):
                dc.SetBrush(wx.Brush(colour))
                dc.SetPen(wx.Pen(colour))
                w = rect.width * (float(value) / self._range)
                r = copy.copy(rect)
                r.width = w
                dc.DrawRectangleRect(r)

        dc.SetTextForeground(wx.Colour(255,255,255))
        font1 = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font1)
        if self._overdrive > self._range:
            value = self._overdrive
            
        if self._skipDigits == True:
            dc.DrawLabel("%d%%" % (value*100/self._range), rect, wx.ALIGN_CENTER)
        else:
            dc.DrawLabel("%.1f%%" % (value * 100 / self._range) , rect, wx.ALIGN_CENTER)

    def OUT_QUAD (self, t, b, c, d):
        t=float(t)
        b=float(b)
        c=float(c)
        d=float(d)
        
        t/=d
        return -c *(t)*(t-2) + b

    def OnTimer(self,event):
        """
        Handles the ``wx.EVT_TIMER`` event for L{PyGauge}.

        :param `event`: a timer event
        """
        oldValue=self._oldValue
        value=self._value[0]

        direction=1

        if oldValue < value:
            direction = 1
            start = 0
            end = value-oldValue
        else:
            start = 0
            end = oldValue - value
            direction = -1
        step=self.OUT_QUAD(self._animStep, start, end, self._animDuration)
        self._animStep += self._period
        
        if self._timerId == event.GetId():
            stop_timer = False
            self._timerOn=1

            if self._animStep > self._animDuration:
                stop_timer = True

            if direction == 1:
                if step < value:
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
                self._timerOn=0
            self.SortForDisplay()

            self.Refresh()


    def Update(self, value, time=0, index=0):
        """
        Update the gauge by adding value to it over time milliseconds. Time
        must be a multiple of 50 milliseconds.

        :param `value`: The value to be added to the gauge.
        :param `time`: The length of time in ms that it will take to move the gauge
        """
        time=abs(value)*50
        if time>500: time=500
        if time == 0: time=500
        if type(value) != type([]):
            value = [value]

        if len(value) != len(self._value):
            raise Exception("ERROR:\n len(value) != len(self.GetValue()) ")

        self._update_value = []
        self._update_step  = []
        for i, v in enumerate(self._value):
            if value[i]+v < 0 or value[i]+v > self._range:
                raise Exception("ERROR2:\n Gauge value must be between 0 and it's range. ")

            self._update_value.append( value[i] +v )
            self._update_step.append(  float(value[i]) / ( time/50 ) )

        #print self._update_

        if not self._timer:
            self._timer = wx.Timer(self, self._timerId)

        self._timer.Start(100)

    def SortForDisplay(self):
        """ Internal method which sorts things so we draw the longest bar first. """

        if self.GetBarGradient():
            tmp = sorted(zip(self._value,self._barGradient)); tmp.reverse()
            a,b = zip(*tmp)
#            self._valueSorted       = list(a)
            self._barGradientSorted = list(b)
        else:
            tmp = sorted(zip(self._value,self._barColour)); tmp.reverse()
            a,b = zip(*tmp)
#            self._valueSorted     = list(a)
            self._barColourSorted = list(b)


