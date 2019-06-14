# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import math

# noinspection PyPackageRequirements
import wx


class VectorPicker(wx.Control):

    myEVT_VECTOR_CHANGED = wx.NewEventType()
    EVT_VECTOR_CHANGED = wx.PyEventBinder(myEVT_VECTOR_CHANGED, 1)

    def __init__(self, *args, **kwargs):
        self._label = str(kwargs.pop('label', ''))
        self._labelpos = int(kwargs.pop('labelpos', 0))
        self._offset = float(kwargs.pop('offset', 0))
        self._size = max(0, float(kwargs.pop('size', 50)))
        self._fontsize = max(1, float(kwargs.pop('fontsize', 8)))
        wx.Control.__init__(self, *args, **kwargs)
        self._font = wx.Font(self._fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        self._angle = 0
        self._length = 1
        self._left = False
        self._right = False
        self._tooltip = 'Click to set angle and velocity, right-click for increments; mouse wheel for velocity only'
        self.SetToolTip(wx.ToolTip(self._tooltip))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)

    def DoGetBestSize(self):
        return wx.Size(self._size, self._size)

    def AcceptsFocusFromKeyboard(self):
        return False

    def GetValue(self):
        return self._angle, self._length

    def GetAngle(self):
        return self._angle

    def GetLength(self):
        return self._length

    def SetValue(self, angle=None, length=None):
        if angle is not None:
            self._angle = min(max(angle, -180), 180)
        if length is not None:
            self._length = min(max(length, 0), 1)
        self.Refresh()

    def SetAngle(self, angle):
        self.SetValue(angle, None)

    def SetLength(self, length):
        self.SetValue(None, length)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        width, height = self.GetClientSize()
        if not width or not height:
            return

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.Clear()
        dc.SetTextForeground(wx.Colour(0))
        dc.SetFont(self._font)

        radius = min(width, height) / 2 - 2
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawCircle(radius + 2, radius + 2, radius)
        a = math.radians(self._angle + self._offset)
        x = math.sin(a) * radius
        y = math.cos(a) * radius
        dc.DrawLine(radius + 2, radius + 2, radius + 2 + x * self._length, radius + 2 - y * self._length)
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.DrawCircle(radius + 2 + x * self._length, radius + 2 - y * self._length, 2)

        if self._label:
            labelText = self._label
            labelTextW, labelTextH = dc.GetTextExtent(labelText)
            labelTextX = (radius * 2 + 4 - labelTextW) if (self._labelpos & 1) else 0
            labelTextY = (radius * 2 + 4 - labelTextH) if (self._labelpos & 2) else 0
            dc.DrawText(labelText, labelTextX, labelTextY)

        lengthText = '%d%%' % (100 * self._length,)
        lengthTextW, lengthTextH = dc.GetTextExtent(lengthText)
        lengthTextX = radius + 2 + x / 2 - y / 3 - lengthTextW / 2
        lengthTextY = radius + 2 - y / 2 - x / 3 - lengthTextH / 2
        dc.DrawText(lengthText, lengthTextX, lengthTextY)

        angleText = '%d\u00B0' % (self._angle,)
        angleTextW, angleTextH = dc.GetTextExtent(angleText)
        angleTextX = radius + 2 - x / 2 - angleTextW / 2
        angleTextY = radius + 2 + y / 2 - angleTextH / 2
        dc.DrawText(angleText, angleTextX, angleTextY)

    def OnEraseBackground(self, event):
        pass

    def OnLeftDown(self, event):
        self._left = True
        self.SetToolTip(None)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnLeftUp)
        if not self._right:
            self.Bind(wx.EVT_MOTION, self.OnMotion)
        if not self.HasCapture():
            self.CaptureMouse()
        self.HandleMouseEvent(event)

    def OnRightDown(self, event):
        self._right = True
        self.SetToolTip(None)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.OnRightUp)
        if not self._left:
            self.Bind(wx.EVT_MOTION, self.OnMotion)
        if not self.HasCapture():
            self.CaptureMouse()
        self.HandleMouseEvent(event)

    def OnLeftUp(self, event):
        self.HandleMouseEvent(event)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.OnLeftUp)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST, handler=self.OnLeftUp)
        self._left = False
        if not self._right:
            self.Unbind(wx.EVT_MOTION, handler=self.OnMotion)
            self.SendChangeEvent()
            self.SetToolTip(wx.ToolTip(self._tooltip))
            if self.HasCapture():
                self.ReleaseMouse()

    def OnRightUp(self, event):
        self.HandleMouseEvent(event)
        self.Unbind(wx.EVT_RIGHT_UP, handler=self.OnRightUp)
        self.Unbind(wx.EVT_MOUSE_CAPTURE_LOST, handler=self.OnRightUp)
        self._right = False
        if not self._left:
            self.Unbind(wx.EVT_MOTION, handler=self.OnMotion)
            self.SendChangeEvent()
            self.SetToolTip(wx.ToolTip(self._tooltip))
            if self.HasCapture():
                self.ReleaseMouse()

    def OnMotion(self, event):
        self.HandleMouseEvent(event)
        event.Skip()

    def OnWheel(self, event):
        amount = 0.1 * event.GetWheelRotation() / event.GetWheelDelta()
        self._length = min(max(self._length + amount, 0.0), 1.0)
        self.Refresh()
        self.SendChangeEvent()

    def HandleMouseEvent(self, event):
        width, height = self.GetClientSize()
        if width and height:
            center = min(width, height) / 2
            x, y = event.GetPositionTuple()
            x = x - center
            y = center - y
            angle = self._angle
            length = min((x * x + y * y) ** 0.5 / (center - 2), 1.0)
            if length < 0.01:
                length = 0
            else:
                angle = ((math.degrees(math.atan2(x, y)) - self._offset + 180) % 360) - 180
            if (self._right and not self._left) or event.ShiftDown():
                angle = round(angle / 15.0) * 15.0
                # floor() for length to make it easier to hit 0%, can still hit 100% outside the circle
                length = math.floor(length / 0.05) * 0.05
            if (angle != self._angle) or (length != self._length):
                self._angle = angle
                self._length = length
                self.Refresh()
                if self._right and not self._left:
                    self.SendChangeEvent()

    def SendChangeEvent(self):
        changeEvent = wx.CommandEvent(self.myEVT_VECTOR_CHANGED, self.GetId())
        changeEvent._object = self
        changeEvent._angle = self._angle
        changeEvent._length = self._length
        self.GetEventHandler().ProcessEvent(changeEvent)
